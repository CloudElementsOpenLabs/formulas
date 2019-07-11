#!/usr/bin/env python

import json
import os.path
import sys
import argparse
import base64
import mermaid_template


def _read_file_as_json(f):
    """Reads a file containing JSON into an object

    :f: @todo
    :returns: @todo

    """
    def read_file_as_string(f):
        fd = None
        try:
            fd = open(f, "r")
            return fd.read()
        finally:
            if fd:
                fd.close()

    str = read_file_as_string(f)
    return json.loads(str)


def _generate_mermaid_links(steps, step_name_mapping):
    return "".join(["".join(["            {name}{line}{dest}\n".format(
            name=step_name_mapping[step['name']],
            line=x['line'].format(link_label=x['text']),
            dest=step_name_mapping[x['dest']])
        for x in step['links']]) for step in steps])


def _generate_mermaid_nodes(steps, step_name_mapping):
    return "".join(["            {name}{shape}\n".format(
        name=step_name_mapping[step['name']],
        shape=step['shape'].format(name=step['label'])) for step in steps])


def _generate_mermaid_node_styles(steps, step_name_mapping):
    return "".join(["            {0}\n".format(
            x['shape_style'].format(
                name=step_name_mapping[x['name']]))
        for x in steps if x['shape_style']])


def _generate_mermaid_node_clicks(steps, step_name_mapping):
    return "".join(
        ['            click {nm} "{lk}" "{label}:<br><pre>{js}</pre>"\n'.format(
            nm=step_name_mapping[x['name']],
            lk=x['click_url'],
            label=x['tip_text']['label'],
            js=x['tip_text']['text']) for x in steps if x['tip_text']])


def _sort_steps(trigger, steps):
    '''
    Sorts Steps by layer instead of by 'onSuccess'
    '''

    def add_steps(to_add):
        '''
        Checks if step exists already and adds if not
        '''
        for step in to_add:
            if sorted_steps.count(step) == 0:
                sorted_steps.append(step)

    def get_step(step_name):
        '''
        Returns actual step json based on name
        '''
        for step in steps:
            if step['name'] == step_name:
                return step
        print "                                 ERROR: Step {0}, is being referenced but does not exist!".format(step_name)

    # Get First step from Trigger
    sorted_steps = []
    steps_2_add = trigger['onSuccess']
    steps_2_add.extend(trigger['onFailure'])
    add_steps(steps_2_add)

    # Go through sorted steps, cnt is pointer to current step name
    cnt = 0
    while len(sorted_steps) != cnt:

        # Get step JSON from Steps
        my_step = get_step(sorted_steps[cnt])
        steps_2_add = []
        steps_2_add.extend(my_step['onSuccess'])
        steps_2_add.extend(my_step['onFailure'])
        add_steps(steps_2_add)
        cnt += 1

    # using sorted step names create full step array
    step_array = []
    for name in sorted_steps:
        step_array.append(get_step(name))
    return step_array


def _dict_to_printout(my_dict):
    max_chars = max([len(x) for x in my_dict]) + 2
    my_keys = sorted(my_dict.keys())
    return "<br>".join([
        "{key: >{width}} : {val}".format(
            key=key,
            width=max_chars,
            val=str(my_dict[key]).replace('"', "'"))
        for key in my_keys])

def parse_trigger(trigger_step):
    rtn_step = {
        'name': "trigger",
        'label': "Trigger",
        'links': [
            {
                'text': 'continue',
                'dest': trigger_step['onSuccess'][0],
                'line': '== {link_label} ==>'
            }
        ],
        'type': 'trigger',
        'json': json.dumps(trigger_step, indent=2),
        'tip_text': {
            'label': 'Trigger Element',
            'text': ""
        },
        'shape': "(({name}))",
        'shape_style': None
    }

    # Generate Trigger Tip Text
    trigger_properties = dict(trigger_step['properties'])
    trigger_properties['type'] = trigger_step['type']
    trigger_properties['async'] = trigger_step['async']
    rtn_step['tip_text']['text'] = _dict_to_printout(trigger_properties)

    # Generate Click Text
    rtn_step['click_url'] = encode_data_for_url(
        trigger_step, rtn_step['tip_text']['text'], rtn_step['tip_text']['label'])

    return rtn_step


def parse_step(step_json):
    rtn_steps = []
    rtn_step = {
        'name': step_json['name'],
        'label': step_json['name'].replace("(", "*").replace(")", "*"),
        'type': step_json['type'],
        'json': json.dumps(step_json, indent=2),
        'links': [],
        'shape': get_shape(step_json['type']),
        'shape_style': None
    }

    # Determine Links
    if len(step_json['onSuccess']) > 0:
        rtn_step['links'].append(
            {
                'text': 'success',
                'dest': step_json['onSuccess'][0],
                'line': '-- {link_label} -->'
            })
    if len(step_json['onFailure']) > 0:
        rtn_step['links'].append(
            {
                'text': 'failure',
                'dest': step_json['onFailure'][0],
                'line': '-- {link_label} -->'
            })

    # If success and fail are the same overwrite with continue
    if len(step_json['onSuccess']) > 0 and \
            len(step_json['onFailure']) > 0 and \
            step_json['onSuccess'][0] == step_json['onFailure'][0]:
        rtn_step['links'] = [
            {
                'text': 'continue',
                'dest': step_json['onSuccess'][0],
                'line': '== {link_label} ==>'
            }
        ]

    # Get Tip Text
    rtn_step['tip_text'] = generate_tip_text(step_json)

    # Generate Click Text
    rtn_step['click_url'] = encode_data_for_url(
        step_json, rtn_step['tip_text']['text'], rtn_step['tip_text']['label'])

    # Determine Style
    if step_json['type'] == 'elementRequest' or step_json['type'] == 'request':
        rtn_step['shape_style'] = get_shape_style(
            step_json['properties']['method'])

    # Append to Return
    rtn_steps.append(rtn_step)

    # Check if there is no continuation or only one for filters and loops
    if len(step_json['onSuccess']) == 0 and len(step_json['onFailure']) == 0:
        end_step = {
            'name': "END",
            'label': "END",
            'type': 'end',
            'json': "",
            'links': [],
            'shape': get_shape("end"),
            'shape_style': get_shape_style("generated"),
            'click_url': None,
            'tip_text': None
        }
        rtn_steps.append(end_step)
        rtn_step['links'] = [
            {'text': 'done', 'dest': 'END', 'line': '-. {link_label} .->'}]

    if step_json['type'] == "filter" and len(rtn_step['links']) == 1:
        end_step = {
            'name': "END-{0}-END".format(step_json['name']),
            'label': "END",
            'type': 'end',
            'json': "",
            'links': [],
            'shape': get_shape("end"),
            'shape_style': get_shape_style("generated"),
            'click_url': None,
            'tip_text': None
        }
        if rtn_step['links'][0]['text'] == 'success':
            rtn_steps.append(end_step)
            rtn_step['links'].append(
                {
                    'text': 'failure',
                    'dest': "END-{0}-END".format(step_json['name']),
                    'line': '-. {link_label} .->'
                })
        elif rtn_step['links'][0]['text'] == 'failure':
            rtn_steps.append(end_step)
            rtn_step['links'].append(
                {
                    'text': 'success',
                    'dest': "END-{0}-END".format(step_json['name']),
                    'line': '-. {link_label} .->'
                })

    return rtn_steps


def get_shape(step_type):
    if step_type == "trigger" or step_type == "end":
        return "(({name}))"
    elif step_type == "filter":
        return "{{{name}}}"
    elif step_type == "loop":
        return "(-{name}-)"
    elif step_type == "elementRequest" or step_type == "request":
        return ">{name}]"
    elif step_type == "script":
        return "({name})"
    else:
        return "[{name}]"


def get_shape_style(shape_style):
    template = "style {{name}} {style};"
    shape_style = shape_style.upper()
    if shape_style == 'GENERATED':
        return template.format(style="stroke-width:3px,stroke-dasharray: 5, 5")
    elif shape_style == 'WORMHOLE':
        return template.format(style="fill:#dda7f9,stroke-width:3px,stroke-dasharray: 5, 5")
    elif shape_style == 'GET':
        return template.format(style="stroke:#0f6ab4")
    elif shape_style == 'POST':
        return template.format(style="stroke:#10a54a")
    elif shape_style == 'PATCH':
        return template.format(style="stroke:#D38042")
    elif shape_style == 'PUT':
        return template.format(style="stroke:#C5862B")
    elif shape_style == 'DELETE':
        return template.format(style="stroke:#a41e22")


def generate_tip_text(step_json):
    rtn_tip = {'label': "", 'text': ""}
    if step_json['type'] == 'script' or step_json['type'] == 'filter':
        rtn_tip['label'] = "JavaScript"
        rtn_tip['text'] = javascript_tip_text(step_json['properties']['body'])
    elif step_json['type'] == 'elementRequest':
        rtn_tip['label'] = "Request"
        rtn_tip['text'] = _dict_to_printout(step_json['properties'])
    elif step_json['type'] == 'loop':
        rtn_tip['label'] = "Loop"
        rtn_tip['text'] = _dict_to_printout(step_json['properties'])
    else:
        rtn_tip['label'] = "Other ({0})".format(step_json['type'])
        rtn_tip['text'] = _dict_to_printout(step_json['properties'])
        print "                               WARNING:  found a 'OTHER' step, {0}".format(step_json['type'])
    return rtn_tip


def javascript_tip_text(js_str):
    # replace < with <span><</span> & > with <span>></span>
    js_str = js_str.replace("<", "|thisIsALessThanSign|")
    js_str = js_str.replace(">", "|thisIsAGreaterThanSign|")
    js_str = js_str.replace("|thisIsALessThanSign|", "<span><</span>")
    js_str = js_str.replace("|thisIsAGreaterThanSign|", "<span>></span>")

    # replace \n with <br> but not \\n
    js_str.replace("\\n", "|ThisIsNotTheNewLineYouAreLookingFor|")
    js_str = js_str.replace("\n", "<br>")

    # replace " with \"
    js_str = js_str.replace('"', "'")

    # Put placeholders back
    js_str = js_str.replace("|ThisIsNotTheNewLineYouAreLookingFor|", "\\n")

    return js_str


def encode_data_for_url(step_json, tip_text, tip_label):
    encode_template = "{label}:<br><br><pre>{js}</pre><br>" + \
        "RAW JSON:<br><br><pre>{raw_json}</pre>"
    string_to_encode = encode_template.format(
        label=tip_label,
        js=tip_text,
        raw_json=javascript_tip_text(json.dumps(step_json, indent=2)))
    encode_template_2 = "<html><head><title>{title}</title>" + \
        "</head><body>{stuff}</body></html>"
    string_to_encode2 = encode_template_2.format(
        title=step_json['name'], stuff=string_to_encode)
    encoded_string = base64.b64encode(string_to_encode2)
    return "data:text/html;charset=utf-8;base64,{0}".format(encoded_string)


def parse_configuration(workflow_json):
    basic_config = [
        {
            "key": "Name",
            "value": workflow_json['name']
        },{
            "key": "Single Threaded?",
            "value": workflow_json['singleThreaded']
        },{
            "key": "Active?",
            "value": workflow_json['active']
        },{
            "key": "Number of Steps",
            "value": len(workflow_json['steps'])
        },{
            "key": "Number of Triggers",
            "value": len(workflow_json['triggers'])
        }
    ]

    config_items = workflow_json['configuration']
    config_values = [x for x in config_items if x['type'] == 'value']
    config_elements = [x for x in config_items if x['type'] == 'elementInstance']
    return "<h3>Basic</h3>{basic}<br/><h3>Elements</h3>{elements}<br/><h3>Values</h3>{values}<br/>".format(
        basic=build_table(['key', 'value'], basic_config),
        elements=build_table(['key', 'name', 'required'], config_elements),
        values=build_table(['key', 'name', 'required'], config_values))


def build_table(headers, values):
    template = "<table>{headers}{rows}</table>"
    row_template = "<tr>{values}</tr>"
    header_template = "<th>{key}</th>"
    value_template = "<td>{value}</td>"

    header = row_template.format(values="".join([header_template.format(key=x) for x in headers]))
    rows = "".join(
        [
            row_template.format(values="".join(
                [
                    value_template.format(value=row[x]) for x in headers
                ]
            )) for row in values
        ]
    )
    return template.format(headers=header, rows=rows)

def parse_workflow(wf_file):
    wf_dir = os.path.dirname(wf_file)
    if len(wf_dir) > 0:
        wf_dir = wf_dir + "/"

    # Ensure Workflow File exists and Read
    if not os.path.isfile(wf_file):
        print "Workflow file does not exist: %s" % (wf_file, )
        sys.exit(1)
    workflow = _read_file_as_json(wf_file)
    print "\n       Generating FlowChart for Formla:  {0}".format(workflow['name'])

    # Sort Steps
    sorted_steps = _sort_steps(
        trigger=workflow['triggers'][0],
        steps=workflow['steps'])

    # Parse the Steps
    parsed_steps = [parse_trigger(workflow['triggers'][0])]
    for step in sorted_steps:
        parsed_steps.extend(parse_step(step))

    # this is where the "hyper"link stuff starts
    temp_step_count = {}
    for step in parsed_steps:
        for link in step['links']:
            if temp_step_count.has_key(link['dest']):
                temp_step_count[link['dest']] += 1
            else:
                temp_step_count[link['dest']] = 1

    mass_steps = [key for key, val in temp_step_count.iteritems() if val > 5]

    new_steps_to_add = []
    for replace in mass_steps:
        counter = 0
        for step in parsed_steps:
            if step['name'] == replace:
                if isinstance(step['shape_style'], (str, unicode)):
                    step['shape_style'] = "{og}{new};".format(og=step['shape_style'][0:-1], new="fill:#dda7f9")
                else:
                    step['shape_style'] = "style {{name}} {style};".format(style="fill:#dda7f9")
            for link in step['links']:
                if link['dest'] == replace:
                    new_name = "{}-{}".format(replace, counter)
                    link['dest'] = new_name
                    counter += 1
                    new_steps_to_add.append(
                        {
                            'name': new_name,
                            'label': "{}".format(replace),
                            'type': 'end',
                            'json': "",
                            'links': [],
                            'shape': get_shape("script"),
                            'shape_style': get_shape_style("wormhole"),
                            'click_url': None,
                            'tip_text': None
                        })

    parsed_steps.extend(new_steps_to_add)
    # this is the end of the "hyper"link stuff

    # Generate StepNameMapping
    step_name_mapping = {}
    cnt = 0
    for step in parsed_steps:
        step_name_mapping[step['name']] = "step-{0:03}".format(cnt)
        cnt += 1

    # Determine longest code block, for end spacing
    max_code_block = max([
        step['tip_text']['text'].count('<br>')
        for step in parsed_steps
        if step['tip_text']])
    if max_code_block > 33:
        max_code_block -= 33

    # Construct Mermaid Markdown graph
    mermaid_string = "        graph TD\n{nodes}{links}{styles}{clicks}".format(
        nodes=_generate_mermaid_nodes(
            steps=parsed_steps,
            step_name_mapping=step_name_mapping),
        links=_generate_mermaid_links(
            steps=parsed_steps,
            step_name_mapping=step_name_mapping),
        styles=_generate_mermaid_node_styles(
            steps=parsed_steps,
            step_name_mapping=step_name_mapping),
        clicks=_generate_mermaid_node_clicks(
            steps=parsed_steps,
            step_name_mapping=step_name_mapping))

    # Generate File Name and Open File
    # formula_name = os.path.basename(wf_file).replace('.json', '')
    formula_name = workflow['name']
    for i in [" ", "+", "=", "-", "&", ":", ";", "/"]:
        formula_name = formula_name.replace(i,"")
    full_mermaid_file_name = '{0}Flowchart-{1}.html'.format(
        wf_dir, formula_name)
    mermaid_file = open(full_mermaid_file_name, 'w')

    # Print out Contents
    mermaid_file.write(mermaid_template.HTML_FORMULA_TEMPLATE.format(
        mermaid_title=workflow['name'],
        mermaid_flowchart=mermaid_string,
        mermaid_end_spacing="<br>".join(["" for x in range(0, max_code_block)]),
        mermaid_configuration=parse_configuration(workflow)))

    # Close and Finish
    mermaid_file.close()
    print "         Generated HTML Flowchart File:  {0}\n".format(
        full_mermaid_file_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Build flowchart from a workflow config file')
    parser.add_argument('file', action='store')
    args = parser.parse_args()
    parse_workflow(args.file)
