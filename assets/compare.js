// https://medium.freecodecamp.org/how-to-create-your-first-bar-chart-with-d3-js-a0e8ea2df386

function clean_str2float(str) {
    if(str){
        str = str.replace(/ /g, '').replace(/,/g, '');
        var float = parseFloat(str);
        if(float){
            return float;
        } else {
            return 0
        }
    } else{
        return 0;
    }
}

function clean_str2float_allow_nan(str) {
    if(str){
        str = str.replace(/ /g, '').replace(/,/g, '');
        var float = parseFloat(str);
        if(float){
            return float;
        } else {
            return null;
        }
    } else{
        return null;
    }
}

function percentage_of(input_val, perc_of, multiplier) {
    return input_val / perc_of * multiplier;
}

function compare(url, comp_key){
    console.log('about to parse stuff');

    d3.csv(url).then(function(data) {
        console.log('parsed stuff');

        console.log(data[0]);

        var keys_div = $('#keys');
        var keys_arr = Object.keys(data[0]);
        for (var a in keys_arr){
            keys_div.append("<div class='btn btn-success btn-list-item'>" + keys_arr[a] + "</div>")
        }

        console.log(keys_arr);
        var max_comp_key = 0;
        var min_comp_key = Infinity;

        console.log('about to do minmax')
        for (var a in data) {
            var val = clean_str2float(
                data[a][comp_key]
            );
            if(val > max_comp_key){
                max_comp_key = val;
            }
            if(val < min_comp_key){
                min_comp_key = val;
            }
        }

        console.log('did minmax')


        $('#min_val').text(min_comp_key);
        $('#max_val').text(max_comp_key);

        data = data.slice(0, 100);

        var svgWidth = 1000;
        var svgHeight = 300;
        var svg = d3.select('#svg1')
            .attr("width", svgWidth)
            .attr("height", svgHeight)
            .attr("class", "bar-chart");

        var barPadding = 5;
        var barWidth = (svgWidth / data.length);
        var barChart = svg.selectAll("rect")
            .data(data)
            .enter()
            .append("rect")
            .attr("y", function(d) {
                return svgHeight - percentage_of(
                    clean_str2float(
                        d[comp_key]
                    ),
                    max_comp_key,
                    svgHeight
                );
            })
            .attr("height", function(d) {
                var entry_exit_count = clean_str2float(
                    d[comp_key]
                );
                if(entry_exit_count < 0) {
                    return 0
                }
                return percentage_of(
                    entry_exit_count,
                    max_comp_key,
                    svgHeight
                );
            })
            .attr("width", function(){
                var width = barWidth - barPadding;
                if (width < 1) {
                    return 1
                } else {
                    return width
                }
            })
            .attr("transform", function (d, i) {
                var translate = [barWidth * i, 0];
                return "translate("+ translate +")";
            });

        // $('#output_dump').text(JSON.stringify(data));


        console.log('part 2');
        data = data.slice(0, 10);


        var svg3 = d3.select("#svg3"),
            margin = {
                top: 20,
                right: 20,
                bottom: 30,
                left: 150
            },
            width = +svg3.attr("width") - margin.left - margin.right,
            height = +svg3.attr("height") - margin.top - margin.bottom,
            g = svg3.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var parseTime = d3.timeParse("%d-%b-%y");

        var x = d3.scaleBand()
            .rangeRound([0, width])
            .padding(0.1);

        var y = d3.scaleLinear()
            .rangeRound([height, 0]);



        x.domain(data.map(function (d) {
            return d['Station Name'];
        }));
        y.domain([0, d3.max(data, function (d) {
            return Number(clean_str2float(
                d[comp_key]
            ));
        })]);

        console.log(x);
        console.log(y);

        g.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))



        g.append("g")
            .call(d3.axisLeft(y))
            .append("text")
            .attr("fill", "#000")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end")
            .text("Speed");

        g.selectAll(".bar")
            .data(data)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function (d) {
                return x(d['Station Name']);
            })
            .attr("y", function (d) {
                return y(Number(clean_str2float(
                    d[comp_key]
                )));
            })
            .attr("width", x.bandwidth())
            .attr("height", function (d) {
                return height - y(Number(clean_str2float(
                    d[comp_key]
                )));
            });

        g.selectAll(".tick text").each(function(d) {
            const a = d3.select(this.parentNode).append("a")
                .attr("xlink:href", "https://www." + d + ".com")
                .attr("transform", "rotate(-45)");
            a.node().appendChild(this);
        });
    });

}
