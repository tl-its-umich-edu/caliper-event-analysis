var numEvents = numEvents || 1;

function skipNullOrEmptyValue(key, value) {
    return (
        value == null ||
        (typeof value == 'object' && Object.keys(value).length == 0)
    ) ? undefined : value;
}

// The original find query used the same regex on the object property.
// However, many PR events don't have "problemroulette" in that property.

db.event.find({
    raw: {
        $regex: /problemroulette/
    }
}).sort({
    _id: -1
}).limit(numEvents).toArray().map(function(eventObject) {
    return JSON.stringify(JSON.parse(eventObject.raw),
        skipNullOrEmptyValue);
}).forEach(function(eventJson) {
    print(eventJson)
});
