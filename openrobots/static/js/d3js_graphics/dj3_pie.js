

function my_pie(dataset, label){
    /*
    var dataset = [
            { name: 'Direct', count: 2742 },
            { name: 'Facebook', count: 2242 },
            { name: 'Pinterest', count: 3112 },
            { name: 'Search', count: 937 },
            { name: 'Others', count: 1450 }
        ];
    */

    var total=0;
    dataset.forEach(function(d){
        total+= d.count;
    });

    var pie=d3.pie()
            .value(d => d.count)
            .sort(null);

    var w=300,h=300;
    const wes = d3.select('#chart');
    const horizontal = wes.attr('width');

    const vertical = d3.select('#chart').attr('height');
    const adj = 80;

    var outerRadiusArc=w/2;
    var innerRadiusArc=100;
    var shadowWidth=10;
    var radius = 100;

    var outerRadiusArcShadow=innerRadiusArc+1;
    var innerRadiusArcShadow=innerRadiusArc-shadowWidth;

    var color = d3.scaleOrdinal()
    .range(d3.schemeSet3)

    var svg=d3.select("#chart")
        .append("svg")
        .attr('viewBox','-' + adj + ' -' + adj + ' ' + (w + 2*adj) + ' ' + (h + adj ))
        .attr("width" , w)
        .attr("height" ,h)
        //.classed("shadow", true)
        .attr("class","shadow")
        .append("g")
        .attr("transform","translate("+w/2+","+h/2+")")
        ;

    var createChart=function(svg,outerRadius,innerRadius,fillFunction,className){

        var arc=d3.arc()
                .innerRadius(outerRadius)
                .outerRadius(innerRadius);

        classString = '.' + className

        var path=svg.selectAll(classString)
            .data(pie(dataset))
            .enter()
            .append("path")
            .attr("d",arc)
            .attr("fill",fillFunction)
            .attr("class",className);

        path.transition()
                    .duration(1000)
                    .attrTween('d', function(d) {
                        var interpolate = d3.interpolate({startAngle: 0, endAngle: 0}, d);
                        return function(t) {
                            return arc(interpolate(t));
                        };
                    });

        var chart={path:path,arc:arc};

        return chart;
    };

    // Draw outer circle
    var mainChart=createChart(svg,outerRadiusArc,innerRadiusArc,function(d,i){
            return color(d.data.name);
        },'path1');
    // Add inner circle
    var shadowChart=createChart(svg,outerRadiusArcShadow,innerRadiusArcShadow,function(d,i){
            var c=d3.hsl(color(d.data.name));
            return d3.hsl((c.h+5), (c.s -.07), (c.l -.15));
        },'path2');


    // Add the polylines between chart and labels:
    var linesForLabel = function(outRadius,innerRadius){

        var innerArc = d3.arc()
        .innerRadius(outRadius * 0.9)
        .outerRadius(innerRadius * 0.9);

        var outerArc = d3.arc()
        .innerRadius(outRadius * 1.1)
        .outerRadius(innerRadius * 1.4);


        var lines= svg
            .selectAll('allPolylines')
            .data(pie(dataset))
            .enter()
            .append('polyline')
                .attr("stroke", "black")
                .style("fill", "none")
                .attr("stroke-width", 1)
                .attr('points', function(d) {
                var posA = innerArc.centroid(d) // line insertion in the slice
                var posB = outerArc.centroid(d) // line break: we use the other arc generator that has been built only for that
                var posC = outerArc.centroid(d) // Label position = almost the same as posB
                var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2 // we need the angle to see if the X position will be at the extreme right or extreme left
                posC[0] = outRadius * 1.0 * (midangle < Math.PI ? 1 : -1); // multiply by 1 or -1 to put it on the right or on the left
                return [posA, posB, posC]
                });

        svg
        .selectAll('allLabels')
        .data(pie(dataset))
        .enter()
        .append('text')
            .text( function(d) { console.log('valor de texto es: ',d.data.name); return d.data.name } )
            .attr('transform', function(d) {
                var pos = outerArc.centroid(d);
                var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
                pos[0] = outRadius * 0.99 * (midangle < Math.PI ? 1 : -1);
                return 'translate(' + pos + ')';
            })
            .style('text-anchor', function(d) {
                var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
                return (midangle < Math.PI ? 'start' : 'end')
            })

    };

    //var grapicLines=linesForLabel(outerRadiusArc,innerRadiusArc);
    var grapicLines= function(){
        linesForLabel(outerRadiusArc, innerRadiusArc )};

    function numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    var addText= function (text,y,size) {
        svg.append('text')
                .text(text)
                .attr('text-anchor','middle')
                .attr('y', y)
                .style('fill','#929DAF')
                .style('font-size', size);
    };

    var restOfTheData=function(){
        addText(d => numberWithCommas(total),0,'20px');
        addText(label,25,'18px');
    };






    setTimeout(grapicLines,1300);
    setTimeout(restOfTheData,1000);




}
