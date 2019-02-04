/**
 * Created by xianyuel on 7/24/17.
 */

var courseChart = dc.pieChart("#chart-course");
var weekdayChart = dc.barChart("#chart-weekday");
var hourChart = dc.barChart("#chart-hour");
var dateChart = dc.lineChart("#chart-date");
var volumeChart = dc.barChart("#chart-range-date");
var charts = [courseChart, weekdayChart, hourChart, dateChart, volumeChart];

d3.json("login_time.json").get(function(error, data){

    if (error) throw error;

    // format raw data
    data.forEach(function(d){
        d.eventTime = new Date(d.eventTime);
        d.course = d.course !== null ? d.course : "Unknown";
    });

    // crossfilter (index) data, create dimensions & groups
    var facts = crossfilter(data);

    var courseDimension = facts.dimension(function(d){ return d.course; });
    var courseGroup = courseDimension.group();

    var weekdayDimension = facts.dimension(function(d){ return d3.time.format("%a")(d.eventTime); });   // abbreviated weekday name
    var weekdayGroup = weekdayDimension.group();

    var hourDimension = facts.dimension(function(d){ return d.eventTime.getHours(); });
    var hourGroup = hourDimension.group();

    var dateDimension = facts.dimension(function(d){ return d.eventTime; });
    var dateGroup = dateDimension.group(function(d){ return new Date(d3.time.format("%x")(d)); });

    // Login by course chart
    courseChart
        .dimension(courseDimension)
        .group(courseGroup)
        .radius(90)
        .innerRadius(40)
        .ordinalColors(colorbrewer.RdBu[9])
        .renderLabel(false)
        .width(350)
        .legend(dc.legend().x(0).y(15).itemHeight(12).gap(8))
        .title(function(d){
            return d.key + ": " + d.value + " -> " + ((d.value/facts.groupAll().value())*100).toFixed(1) + "%";
        })
    ;

    // Login by weekday chart
    weekdayChart
        .dimension(weekdayDimension)
        .group(weekdayGroup)
        .x(d3.scale.ordinal().domain(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]))
        .xUnits(dc.units.ordinal)
        .colorAccessor(function(d) {return d.key; })
        .ordinalColors(colorbrewer.Blues[7])
        .colorDomain(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
        .elasticY(true)
        .renderHorizontalGridLines(true)
        .barPadding(0.12)
        .outerPadding(0.12)
        .width(300)
        .margins({top: 10, right: 20, bottom: 20, left: 40})
    ;

    // Login by hour chart
    hourChart
        .dimension(hourDimension)
        .group(hourGroup)
        .x(d3.scale.linear().domain([0, 24]))
        .round(Math.floor)
        .brushOn(true)
        .elasticY(true)
        .colorAccessor(function(d) {return d.key; })
        .colors(colorbrewer.RdBu[4])
        .colorDomain([0, 24])
        .renderHorizontalGridLines(true)
        .width(450)
        .margins({top: 10, right: 5, bottom: 20, left: 40})
        .filterPrinter(function (filters) {
            var lowHour = filters[0][0];
            var upHour = filters[0][1];
            return "["+lowHour+":00 -> "+upHour+":00]";
        })
    ;

    // Login by date chart & its range chart
    dateChart
        .dimension(dateDimension)
        .group(dateGroup)
        .x(d3.time.scale().domain([dateDimension.bottom(1)[0].eventTime, dateDimension.top(1)[0].eventTime]))
        .rangeChart(volumeChart)
        .elasticY(true)
        .brushOn(false)
        .renderHorizontalGridLines(true)
        .renderArea(true)
        .width(1200)
        .margins({top: 20, right: 0, bottom: 20, left: 40})
        .title(function(d){
            return d3.time.format("%x")(d.key) + ": " + d.value;
        })
    ;

    volumeChart
        .dimension(dateDimension)
        .group(dateGroup)
        .x(d3.time.scale().domain([dateDimension.bottom(1)[0].eventTime, dateDimension.top(1)[0].eventTime]))
        .centerBar(true)
        .width(1200)
        .height(40)
        .margins({top: 0, right: 0, bottom: 20, left: 40})
    ;


    dc.renderAll();

});
