let arr = steps.aggregator ? steps.aggregator.arr : [];

arr.push(steps.loopThroughInvoiceLines.entry.amount)

done({
  arr: arr
})