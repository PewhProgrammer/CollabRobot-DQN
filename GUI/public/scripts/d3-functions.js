
var margin = {top: 50, right: 20, bottom: 30, left: 100},
width = 500 - margin.left - margin.right,
height = 300 - margin.top - margin.bottom;


var x = d3.scale.linear()
.range([0, width]);

var y0 = d3.scale.linear()
.range([height, 0]);

var y1 = d3.scale.linear()
.range([height, 0]);

var xAxis = d3.svg.axis()
.scale(x)
.orient("bottom");

var y0Axis = d3.svg.axis()
.scale(y0)
.orient("left");

var y1Axis = d3.svg.axis()
.scale(y1)
.orient("left");

/*var bisectX = d3.bisector(function(d) { return d.Episode; }).left;

var y0line = d3.svg.line()
.x(function(d) { return x(d.Episode); })
.y(function(d) { return y0(d.Reward); });

var bline = d3.svg.line()
.x(function(d) { return x(d.Episode); })
.y(function(d) { return y0(0); });

var y1line = d3.svg.line()
.x(function(d) { return x(d.Episode); })
.y(function(d) { return y1(d.Length); });

var svg = d3.select(".graphHolder")
.attr("width", width + margin.left + margin.right)
.attr("height", height *2.5 + margin.top + margin.bottom);
var g1 = svg.append("g")
.attr("class","graphA")
.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
var g2 = svg.append("g")
.attr("class","graphB")
.attr("transform", "translate(" + margin.left + "," + (margin.top + height + 50) +  ")");

var actionSVG = d3.select(".Qholder")
    .attr("width", width*1.5 + margin.left + margin.right)
    .attr("height", height *2.5 + margin.top + margin.bottom);
*/
    
var currentEx = 0;
var currentState = 0;
var maxEx = 0;

var canResetLine = true;
var goingForward = false;
var goingBackward = false;
var lastState = false;
var globalData = null;

globalData = data;

g1.append("g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + height + ")")
  .call(xAxis);
  
g2.append("g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + height + ")")
  .call(xAxis);

g1.append("g")
  .attr("class", "y0 axis")
  .style("fill","steelblue")
  .call(y0Axis)
.append("text")
  .attr("transform", "rotate(-0)")
  .attr("y", -20)
  .attr("x",-30)
  .attr("dy", ".71em")
  .attr("font-size",'14px')
  .text("Reward");

g2.append("g")
  .attr("class", "y1 axis")
  .style("fill","green")
  .call(y1Axis)
.append("text")
  .attr("transform", "rotate(-0)")
  .attr("y", -20)
  .attr("x",-30)
  .attr("dy", ".71em")
  .attr("font-size",'14px')
  .text("Episode length");

g1.append("path")
  .datum(data)
  .attr("class", "y0line")
  .attr("d", y0line(data));

g2.append("path")
  .datum(data)
  .attr("class", "y1line")
  .attr("d", y1line(data));
  
g1.append("path")
    .datum(data)
    .attr("class", "bline")
    .style("stroke-dasharray", ("3, 3"))
    .attr("d", bline(data));
    
var focusA = g1.append("g")
  .attr("class", "focus focusA")
  .style("display", null);

focusA.append("line")
  .attr("y1", 0)
  .attr("y2", height)
  .attr("x0",0)
  .attr("x1",1)
  .attr("opacity",0.5)
  .style("stroke","steelblue")
  .style("stroke-width",1);

focusA.append("text")
  .attr("x", -10)
  .attr("y", -5)
  .attr("fill","steelblue")
  .attr("dy", ".35em");
  
var focusB = g1.append("g")
  .attr("class", "focus focusB")
  .style("display", null);

focusB.append("line")
  .attr("y1", 0)
  .attr("y2", height)
  .attr("x0",0)
  .attr("x1",1)
  .attr("opacity",0.5)
  .style("stroke","green")
  .style("stroke-width",1);

focusB.append("text")
  .attr("x", -10)
  .attr("y", -5)
  .attr("fill","green")
  .attr("dy", ".35em");

g1.append("rect")
  .attr("class", "overlay")
  .attr("id","overlayA")
  .attr("width", width)
  .attr("height", height)
  .on("mouseover", function() {canResetLine = false;})
  .on("mouseleave",function() {canResetLine = true;})
  .on("mousemove", mousemoveG1)
  .on("mousedown", setEpisode);
  
g2.append("rect")
  .attr("class", "overlay")
  .attr("id","overlayB")
  .attr("width", width)
  .attr("height", height)
  .on("mouseover", function() {canResetLine = false;})
  .on("mouseleave",function() {canResetLine = true;})
  .on("mousemove", mousemoveG2)
  .on("mousedown", setEpisode);

function setEpisode() {
    var x0 = x.invert(d3.mouse(this)[0]),
    i = bisectX(data, x0, 1),
    d0 = data[i - 1],
    d1 = data[i],
    d = x0 - d0.Episode > d1.Episode - x0 ? d1 : d0;
    currentEx = i
    currentState = 0;
    canResetLine = true;
    updateData();
}

function mousemoveG1() {
var x0 = x.invert(d3.mouse(this)[0]),
    i = bisectX(data, x0, 1),
    d0 = data[i - 1],
    d1 = data[i],
    d = x0 - d0.Episode > d1.Episode - x0 ? d1 : d0;
focusA.attr("transform", "translate(" + x(d.Episode) + "," + 0 + ")");
focusA.select("text").text(Number(d.Reward).toFixed(2))
canResetLine = false;;
}

function mousemoveG2() {
var x0 = x.invert(d3.mouse(this)[0]),
    i = bisectX(data, x0, 1),
    d0 = data[i - 1],
    d1 = data[i],
    d = x0 - d0.Episode > d1.Episode - x0 ? d1 : d0;
focusB.attr("transform", "translate(" + x(d.Episode) + "," + (height+50) + ")");
focusB.select("text").text(Number(d.Length).toFixed(2))
canResetLine = false;
}
    
currentEx = data.length-1;

});


function returnColor(number) {
if (number < 0) {
    return "red";
}
else { return "green";}
}

function returnSize(number) {
var toReturn = Math.abs(number);
toReturn = toReturn *10;
if (toReturn > 35) {toReturn = 35;}
if (toReturn < 5) {toReturn = 5;}
return toReturn;

}

var inter = setInterval(function() {
            updateData();
    }, 1000); 
    
var moveForward = setInterval(function() {
        
        if (goingForward == true) {console.log("I'm being pressed"); forwardEX();} ;},10);

var moveBackward = setInterval(function() {
        if (goingBackward == true) {backEX();} ;},10);
    
function getLine(action) {
return [105 + 100*action,205 + 100*action];
}

function getSquare(action) {
return 105 + 100*action;

}

function labelAction(action) {
if (action == 0) {return "Up";}
if (action == 1) {return "Down";}
if (action == 2) {return "Left";}
if (action == 3) {return "Right";}
}

function backEX() {
currentEx = currentEx - 1;
currentState = 0;
if (currentEx < 0) {currentEx = 0;};
updateData();
}

function forwardEX() {
currentEx = currentEx + 1;
currentState = 0;
if (currentEx > maxEx) {currentEx = maxEx;};
updateData();
}

function forwardHover() {
var canHover = d3.select(".forwardEx").attr("opacity");
}

function forwardEXPre() {
goingForward = true;
}

function forwardEXPost() {
goingForward = false;
}

function backEXPre() {
goingBackward = true;
}

function backEXPost() {
goingBackward = false;
}


d3.selectAll(".moveButton").on("mouseover",function() {
if (d3.select(this).select("image").attr("opacity") != 0.1) {
d3.select(this).select("circle").transition().duration(100)
    .attr("fill-opacity","0.5");
    };

});

d3.selectAll(".moveButton").on("mouseleave",function() {
if (d3.select(this).select("image").attr("opacity") != 0.1) {
d3.select(this).select("circle").transition().duration(100)
    .attr("fill-opacity","0.1");
};
});

updateData();

function updateData() {

// Get the data again
d3.csv("log.csv", function(error, data) {
       data.forEach(function(d) {
        d.Episode = +d.Episode;
        d.Reward = +d.Reward;
        d.Length = +d.Length;
    });

    // Scale the range of the data again 
  x.domain(d3.extent(data, function(d) { return d.Episode; }));
  y0.domain(d3.extent(data, function(d) { return d.Reward; }));
  y1.domain(d3.extent(data, function(d) { return d.Length; }));

// Select the section we want to apply our changes to
var g1 = d3.select(".graphA").transition();
var g2 = d3.select(".graphB").transition();
//var line = d3.svg.line()
//    .x(function(d) { return x(d.Episode); })
//    .y(function(d) { return y(d.Reward); });
    
// Make the changes
    g1.select(".y0line")   // change the line
        .duration(500)
        .attr("d", y0line(data));
        
    g2.select(".y1line")   // change the line
        .duration(500)
        .attr("d", y1line(data));
        
    g1.select(".bline").duration(500)
        .attr("d", bline(data));

    g1.select(".x.axis") // change the x axis
        .duration(750)
        .call(xAxis);
        
    g2.select(".x.axis") // change the x axis
        .duration(750)
        .call(xAxis);
        
    
        
    g1.select(".y0.axis") // change the y axis
        .duration(500)
        .call(y0Axis);
    g2.select(".y1.axis") // change the z axis
        .duration(500)
        .call(y1Axis);
        
        
     var focusA = d3.select(".focusA");
     var focusB = d3.select(".focusB");   
     
d3.selectAll("overlay").remove()
d3.select(".graphA").append("rect")
  .attr("class", "overlay")
  .attr("id","overlayA")
  .attr("width", width)
  .attr("height", height)
  .on("mouseover", function() {canResetLine = false;})
  .on("mouseleave",function() {canResetLine = true;})
  .on("mousemove", mousemoveG1B)
  .on("mousedown", setEpisodeB);
  
d3.select(".graphB").append("rect")
  .attr("class", "overlay")
  .attr("id","overlayB")
  .attr("width", width)
  .attr("height", height)
  .on("mouseover", function() {canResetLine = false;})
  .on("mouseleave",function() {canResetLine = true;})
  .on("mousemove", mousemoveG2B)
  .on("mousedown", setEpisodeB);
     
function setEpisodeB() {
    var x0 = x.invert(d3.mouse(this)[0]),
    i = bisectX(data, x0, 1),
    d0 = data[i - 1],
    d1 = data[i],
    d = x0 - d0.Episode > d1.Episode - x0 ? d1 : d0;
    currentEx = i
    currentState = 0;
    canResetLine = true;
    updateData();
}
     
    function mousemoveG1B() {
        var x0 = x.invert(d3.mouse(this)[0]),
            i = bisectX(data, x0, 1),
            d0 = data[i - 1],
            d1 = data[i],
            d = x0 - d0.Episode > d1.Episode - x0 ? d1 : d0;
        focusA.attr("transform", "translate(" + x(d.Episode) + "," + 0 + ")");
        focusA.select("text").text(Number(d.Reward).toFixed(2))
        canResetLine = false;;
      }

    function mousemoveG2B() {
        var x0 = x.invert(d3.mouse(this)[0]),
            i = bisectX(data, x0, 1),
            d0 = data[i - 1],
            d1 = data[i],
            d = x0 - d0.Episode > d1.Episode - x0 ? d1 : d0;
        focusB.attr("transform", "translate(" + x(d.Episode) + "," + (height+50) + ")");
        focusB.select("text").text(Number(d.Length).toFixed(2))
        canResetLine = false;
      }
        
d3.select(".eT").text("Episode : " + Number(data.slice(currentEx)[0].Episode).toLocaleString());
        
d3.csv(data.slice(currentEx)[0].LOG, function(error,data) {
    d3.select(".acT").text("Action : " + labelAction(data.slice(currentState)[0].ACTION));
    d3.select(".rT").text("Reward : " + Number(data.slice(currentState)[0].REWARD).toFixed(2));
    d3.select(".sT").text("State : " + (currentState +1) + " / " + data.length);
    d3.select(".abox").transition().duration(500).attr("transform", "translate(" + getSquare(data.slice(currentState)[0].ACTION) + "," + 330 + ")")
    var linePos = getLine(data.slice(currentState)[0].ACTION);
    d3.select(".aline").transition().duration(500).attr('x1',linePos[0]).attr('x2',linePos[1]);

    var vC = d3.select(".valueCircle")
        vC.transition().duration(500).attr('r',returnSize(data.slice(currentState)[0].V))
            .attr("fill",returnColor(data.slice(currentState)[0].V))
            .attr("stroke",returnColor(data.slice(currentState)[0].V));
        vC.select("title").text(data.slice(currentState)[0].V);
        d3.select(".vt").text(Number(data.slice(currentState)[0].V).toFixed(2));

    var A0C = d3.select(".a0")
        A0C.transition().duration(500).attr('r',returnSize(data.slice(currentState)[0].A0))
            .attr("fill",returnColor(data.slice(currentState)[0].A0))
            .attr("stroke",returnColor(data.slice(currentState)[0].A0));
        A0C.select("title").text(data.slice(currentState)[0].A0);
        d3.select(".a0t").text(Number(data.slice(currentState)[0].A0).toFixed(2));
    
    var A1C = d3.select(".a1")
        A1C.transition().duration(500).attr('r',returnSize(data.slice(currentState)[0].A1))
            .attr("fill",returnColor(data.slice(currentState)[0].A1))
            .attr("stroke",returnColor(data.slice(currentState)[0].A1));
        A1C.select("title").text(data.slice(currentState)[0].A1);
        d3.select(".a1t").text(Number(data.slice(currentState)[0].A1).toFixed(2));
    
    var A2C = d3.select(".a2")
        A2C.transition().duration(500).attr('r',returnSize(data.slice(currentState)[0].A2))
            .attr("fill",returnColor(data.slice(currentState)[0].A2))
            .attr("stroke",returnColor(data.slice(currentState)[0].A2));
        A2C.select("title").text(data.slice(currentState)[0].A2);
        d3.select(".a2t").text(Number(data.slice(currentState)[0].A2).toFixed(2));
    
    var A3C = d3.select(".a3")
        A3C.transition().duration(500).attr('r',returnSize(data.slice(currentState)[0].A3))
            .attr("fill",returnColor(data.slice(currentState)[0].A3))
            .attr("stroke",returnColor(data.slice(currentState)[0].A3));
        A3C.select("title").text(data.slice(currentState)[0].A3);
        d3.select(".a3t").text(Number(data.slice(currentState)[0].A3).toFixed(2));

    if (currentState + 1 < data.length) 
            {currentState = currentState + 1;} 
        else if (currentState + 1 == data.length && lastState == false)
            {currentState = currentState; lastState = true;}
        else if (currentState + 1 == data.length && lastState == true) 
            {currentState = 0; lastState = false;}
});

var currentIMG = d3.select('.exampleIMG').attr("href").substring(0,d3.select('.exampleIMG').attr("href").length-12);
if (data.slice(currentEx)[0].IMG != currentIMG) {
    currentState = 0;
    var randAdd = Math.floor((Math.random() * 10000) + 1);
    d3.select('.exampleIMG').remove();
    d3.select('.Qholder').append("image")
        .attr("class",'exampleIMG')
        .attr("transform", "translate(" + 180 + "," + 50 + ")")
        .attr("opacity",0.0)
        .attr("width",'200px')
        .attr("height",'200px')
        .attr("href",data.slice(currentEx)[0].IMG + "?random=" + randAdd)
        .transition().delay(50)
        .attr("opacity",1.0);
    clearInterval(inter);
    inter = setInterval(function() {
            updateData();
    }, 1000); 
};


    
    d3.select('.backEx').attr('opacity',function() {if (currentEx == 0) {return 0.1;} else {return 0.9;}});
    d3.select('.forwardEx').attr('opacity',function() {if (currentEx == data.length-1) {return 0.1;} else {return 0.9;}});
    d3.select('.bcir').attr('fill-opacity',function() {if (currentEx == 0) {return 0.05;} else {return d3.select('.bcir').attr('fill-opacity');}});
    d3.select('.fcir').attr('fill-opacity',function() {if (currentEx == data.length-1) {return 0.05;} else {return d3.select('.fcir').attr('fill-opacity');}});
    
    if (canResetLine == true) {
        d3.select(".focusA").transition().attr("transform", "translate(" + x(data.slice(currentEx)[0].Episode) + "," + 0 + ")")
            .select("text").text(Number(data.slice(currentEx)[0].Reward).toFixed(2));
        d3.select(".focusB").transition().attr("transform", "translate(" + x(data.slice(currentEx)[0].Episode) + "," + (height+50) + ")")
            .select("text").text(Number(data.slice(currentEx)[0].Length).toFixed(2));
        }
maxEx = data.length-1;
});

}
