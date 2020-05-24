function my_pie(dataset){
/*
var dataset = [
        { name: 'Direct', count: 2742 },
        { name: 'Facebook', count: 2242 },
        { name: 'Pinterest', count: 3112 },
        { name: 'Search', count: 937 },
        { name: 'Others', count: 1450 }
    ];
*/
//var dataset = {{data|safe}}

var total=0;

dataset.forEach(function(d){
    total+= d.count;
});
var pie_data=d3.pie()
            .value(function(d){return d.count})
            .sort(null);
var pie=d3.pie()
        .value(function(d){return d.count})
        .sort(null);
var w=300,h=300;
const adj = 60;

var outerRadiusArc=w/2;
var innerRadiusArc=100;
var shadowWidth=10;

var outerRadiusArcShadow=innerRadiusArc+1;
var innerRadiusArcShadow=innerRadiusArc-shadowWidth;


var color = d3.scaleOrdinal()
    .range(['#41B787', '#6352B9', '#B65480', '#D5735A', '#D7D9DA']);

//Create the svg and a group inside it.

var svg=d3.select("#chart")
    .append("svg")
    .attr('viewBox','-' + adj + ' -' + adj + ' ' + (w + adj) + ' ' + (h + adj ))
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

    var path=svg.selectAll(classString).data(pie_data(dataset))
    .enter().append("path").attr("d",arc).attr("fill",fillFunction)
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



var mainChart=createChart(svg,outerRadiusArc,innerRadiusArc,function(d,i){
        return color(d.data.name);
    },'path1');

var shadowChart=createChart(svg,outerRadiusArcShadow,innerRadiusArcShadow,function(d,i){
        var c=d3.hsl(color(d.data.name));
        return d3.hsl((c.h+5), (c.s -.07), (c.l -.15));
    },'path2');


//Add text

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

var addText= function (text,y) {
    svg.append('text')
            .text(text)
            .attr("y",y)
            .attr("x",-35)
            ;
};

var restOfTheData=function(){

    addText(function(){
        return numberWithCommas(total);
    },0);


    addText(function(){
        return "Page View";
    },25);

};


setTimeout(restOfTheData,1000);

}
