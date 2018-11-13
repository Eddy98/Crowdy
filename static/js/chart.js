var data = [{"time": "12am", "quantity": 24},
    {"time": "1am", "quantity": 15},
    {"time": "2am", "quantity": 3},
    {"time": "3am", "quantity": 2},
    {"time": "4am", "quantity": 30},
    {"time": "5am", "quantity": 21},
    {"time": "6am", "quantity": 13},
    {"time": "7am", "quantity": 15},
    {"time": "8am", "quantity": 3},
    {"time": "9am", "quantity": 2},
    {"time": "10am", "quantity": 30},
    {"time": "11am", "quantity": 21},
    {"time": "12pm", "quantity": 13},
    {"time": "1pm", "quantity": 15},
    {"time": "2pm", "quantity": 3},
    {"time": "3pm", "quantity": 2},
    {"time": "4pm", "quantity": 30},
    {"time": "5pm", "quantity": 21},
    {"time": "6pm", "quantity": 13},
    {"time": "7pm", "quantity": 15},
    {"time": "8pm", "quantity": 3},
    {"time": "9pm", "quantity": 2},
    {"time": "10pm", "quantity": 30},
    {"time": "11pm", "quantity": 21}];
window.onload = function () {

    let margin = {top: 10, right: 10, bottom: 90, left: 10};

    let width = 960 - margin.left - margin.right;

    let height = 500 - margin.top - margin.bottom;

    let xScale = d3.scale.ordinal().rangeRoundBands([0, width], .03)

    let yScale = d3.scale.linear()
        .range([height, 0]);


    let xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom");


    let yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left");

    let svgContainer = d3.select("#chartID").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g").attr("class", "container")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    xScale.domain(data.map(function (d) {
        return d.time;
    }));
    yScale.domain([0, d3.max(data, function (d) {
        return d.quantity;
    })]);


//xAxis. To put on the top, swap "(height)" with "-5" in the translate() statement. Then you'll have to change the margins above and the x,y attributes in the svgContainer.select('.x.axis') statement inside resize() below.
    let xAxis_g = svgContainer.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + (height) + ")")
        .call(xAxis)
        .selectAll("text");

// Uncomment this block if you want the y axis
    /*var yAxis_g = svgContainer.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6).attr("dy", ".71em")
            //.style("text-anchor", "end").text("Number of Applicatons");
    */

    svgContainer.selectAll(".bar")
        .data(data)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", function (d) {
            return xScale(d.time);
        })
        .attr("width", xScale.rangeBand())
        .attr("y", function (d) {
            return yScale(d.quantity);
        })
        .attr("height", function (d) {
            return height - yScale(d.quantity);
        });


// Controls the text labels at the top of each bar. Partially repeated in the resize() function below for responsiveness.
    svgContainer.selectAll(".text")
        .data(data)
        .enter()
        .append("text")
        .attr("class", "label")
        .attr("x", (function (d) {
            return xScale(d.time) + xScale.rangeBand() / 2;
        }))
        .attr("y", function (d) {
            return yScale(d.quantity) + 1;
        })
        .attr("dy", ".75em")
        .text(function (d) {
            return d.quantity;
        });


    document.addEventListener("DOMContentLoaded", resize);
    d3.select(window).on('resize', resize);

    function resize() {
        console.log('----resize function----');
        // update width
        width = parseInt(d3.select('#chartID').style('width'), 10);
        width = width - margin.left - margin.right;

        height = parseInt(d3.select("#chartID").style("height"));
        height = height - margin.top - margin.bottom;
        console.log('----resiz width----' + width);
        console.log('----resiz height----' + height);
        // resize the chart

        xScale.range([0, width]);
        xScale.rangeRoundBands([0, width], .03);
        yScale.range([height, 0]);

        yAxis.ticks(Math.max(height / 50, 2));
        xAxis.ticks(Math.max(width / 50, 2));

        d3.select(svgContainer.node().parentNode)
            .style('width', (width + margin.left + margin.right) + 'px');

        svgContainer.selectAll('.bar')
            .attr("x", function (d) {
                return xScale(d.time);
            })
            .attr("width", xScale.rangeBand());

        svgContainer.selectAll("text")
        // .attr("x", function(d) { return xScale(d.time); })
            .attr("x", (function (d) {
                return xScale(d.time) + xScale.rangeBand() / 2;
            }))
            .attr("y", function (d) {
                return yScale(d.quantity) + 1;
            })
            .attr("dy", ".75em");

        svgContainer.select('.x.axis').call(xAxis.orient('bottom')).selectAll("text").attr("y", 10).call(wrap, xScale.rangeBand());
        // Swap the version below for the one above to disable rotating the titles
        // svgContainer.select('.x.axis').call(xAxis.orient('top')).selectAll("text").attr("x",55).attr("y",-25);


    }

    function wrap(text, width) {
        text.each(function () {
            var text = d3.select(this),
                words = text.text().split(/\s+/).reverse(),
                word,
                line = [],
                lineNumber = 0,
                lineHeight = 1.1, // ems
                y = text.attr("y"),
                dy = parseFloat(text.attr("dy")),
                tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
            while (word = words.pop()) {
                line.push(word);
                tspan.text(line.join(" "));
                if (tspan.node().getComputedTextLength() > width) {
                    line.pop();
                    tspan.text(line.join(" "));
                    line = [word];
                    tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
                }
            }
        });
    }
}
