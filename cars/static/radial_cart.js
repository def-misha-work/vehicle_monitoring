"use strict";
(function() {
    var gap = 2;
    var ranDataset = function(container) {
        return [
            { index: 0, name: 'move', icon: "\uF105", percentage: parseInt(container.querySelector('.one').textContent) },
            { index: 1, name: 'exercise', icon: "\uF101", percentage: parseInt(container.querySelector('.two').textContent) },
            { index: 2, name: 'stand', icon: "\uF106", percentage: parseInt(container.querySelector('.three').textContent) }
        ];
    };
    var colors = ["#e90b3a", "#a0ff03", "#1ad5de"];
    var width = 100,
        height = 100,
        τ = 2 * Math.PI;
    function build(container) {
        var dataset = ranDataset(container); // Получаем набор данных из контейнера
        var arc = d3.svg.arc()
            .startAngle(0)
            .endAngle(function(d) {
                return d.percentage / 100 * τ; // Угол на основе процента
            })
            .innerRadius(function(d) {
                return 28 - d.index * (8 + gap);
            })
            .outerRadius(function(d) {
                return 36 - d.index * (8 + gap);
            })
            .cornerRadius(4);
        var background = d3.svg.arc()
            .startAngle(0)
            .endAngle(τ)
            .innerRadius(function(d, i) {
                return 140 - d.index * (40 + gap);
            })
            .outerRadius(function(d, i) {
                return 180 - d.index * (40 + gap);
            });
        var svg = d3.select(container).append("svg") // Используем контейнер
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
        var gradient = svg.append("svg:defs")
            .append("svg:linearGradient")
            .attr("id", "gradient")
            .attr("x1", "0%")
            .attr("y1", "100%")
            .attr("x2", "50%")
            .attr("y2", "0%")
            .attr("spreadMethod", "pad");
        gradient.append("svg:stop")
            .attr("offset", "0%")
            .attr("stop-color", "#fe08b5")
            .attr("stop-opacity", 1);
        gradient.append("svg:stop")
            .attr("offset", "100%")
            .attr("stop-color", "#ff1410")
            .attr("stop-opacity", 1);
        var defs = svg.append("defs");
        var filter = defs.append("filter").attr("id", "dropshadow");
        filter.append("feGaussianBlur").attr("in", "SourceAlpha").attr("stdDeviation", 4).attr("result", "blur");
        filter.append("feOffset").attr("in", "blur").attr("dx", 1).attr("dy", 1).attr("result", "offsetBlur");
        var feMerge = filter.append("feMerge");
        feMerge.append("feMergeNode").attr("in", "offsetBlur");
        feMerge.append("feMergeNode").attr("in", "SourceGraphic");
        var field = svg.selectAll("g")
            .data(dataset)
            .enter().append("g");
        field.append("path").attr("class", "progress").attr("filter", "url(#dropshadow)");
        field.append("path").attr("class", "bg")
            .style("fill", function(d) {
                return colors[d.index];
            })
            .style("opacity", 0.2)
            .attr("d", background)
            .style("fill", "none");
        field.append("text").attr('class', 'icon');
        d3.transition().duration(1750).each(update);
        function update() {
            field = field
                .each(function(d) {
                    this._value = d.percentage;
                })
                .data(dataset)
                .each(function(d) {
                    d.previousValue = this._value;
                });
            field.select("path.progress").transition().duration(1750).delay(function(d, i) {
                return i * 200;
            })
            .ease("elastic")
            .attrTween("d", arcTween)
            .style("fill", function(d) {
                if (d.index === 0) {
                    return "url(#gradient)";
                }
                return colors[d.index];
            });
            field.select("text.icon").text(function(d) {
                return d.icon;
            }).attr("transform", function(d) {
                return "translate(10," + -(150 - d.index * (40 + gap)) + ")";
            });
            field.select("text.completed").text(function(d) {
                return Math.round(d.percentage / 100 * 600);
            });
            setTimeout(update, 2000);
        }
        function arcTween(d) {
            var i = d3.interpolateNumber(d.previousValue, d.percentage);
            return function(t) {
                d.percentage = i(t);
                return arc(d);
            };
        }
    }
    document.querySelectorAll('.chart').forEach(function(container) {
        build(container);
    });
})();