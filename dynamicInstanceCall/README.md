Dynamic element API calls
-------------

The DriveExecution formula lists content for the root directory of a given instance.  The challenge is to do so for a random list of instances found in your Organization.   

#### Prerequisites
* Step "getCurrentToken" builds the authentication header per instance. It requires your User and Organization token
* filterByTag hardcodes on tags named "filterAccount". Change this by whatever you need
* Make sure to have some instances that have the tag set to what you filter on 
* This formula eventually does a /folders/content call. So you should run this formula with dropbox, google drive, ...

#### Formula steps explained

| Step | Explanation           |
| ------------- |:-------------|
| listInstances      | Executes a CE Platform API call to /instances  |
| shortInstanceArr | Irrelevant step but used to limit the results per instance. You can just work with listInstances as well |
| loopInstances | Loops over each entry in the return value of shortInstanceArr |
|getCurrentToken | Since the formula is not launched with element instance variables, it will do its API calls via a regular HTTP element request.  It will still call the actual element instance. This step concatenates the authentication header for the current instance|
|filterByTag| A JS Filter step returning true if the tags hold the information we are looking for. Note that you can move this searchFor as part of the trigger upon launching the formula|
|positive|Log the instance that was found and add to global variable named instanceCounter|
|filesCall| Do the HTTP API call. Again: still to the actual instance but it constructs the instance call manually reusing the Auth header constructed in getCurrentToken|
|endResult|lists us for how many instance we made the actual call|
