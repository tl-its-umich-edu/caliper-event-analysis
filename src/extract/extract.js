const REGEX_FLAG_IGNORE_CASE = 'i';
var numEvents = (typeof numEvents !== 'undefined') ? numEvents : 1;
var rawRegex = (typeof rawRegex !== 'undefined') ? rawRegex : '.*';

function skipNullOrEmptyValue(key, value) {
    return (
        value == null ||
        (typeof value == 'object' && Object.keys(value).length == 0)
    ) ? undefined : value;
}

db.event.find({
    raw: {
        $regex: new RegExp(rawRegex, REGEX_FLAG_IGNORE_CASE)
    }
}).sort({
    _id: -1
}).limit(numEvents).map(function(eventObject) {
    return JSON.stringify(JSON.parse(eventObject.raw),
        skipNullOrEmptyValue);
}).forEach(function(eventJson) {
    print(eventJson)
});
