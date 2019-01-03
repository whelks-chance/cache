// https://medium.freecodecamp.org/how-to-create-your-first-bar-chart-with-d3-js-a0e8ea2df386

function clean_str2float(str) {
    str = str.replace(/ /g, '').replace(/,/g, '');
    // console.log(str);
    var float = parseFloat(str);
    // console.log(float);
    if(float){
        return float;
    } else {
        return 0
    }
}

function percentage_of(input_val, perc_of, multiplier) {
    return input_val / perc_of * multiplier;
}

function compare(url, comp_key){

    d3.csv(url, function(data) {

        console.log(data[0]);

        var keys_div = $('#keys');
        var keys_arr = Object.keys(data[0]);
        for (var a in keys_arr){
            keys_div.append("<div class='btn btn-success btn-list-item'>" + keys_arr[a] + "</div>")
        }

        var max_comp_key = 0;
        var min_comp_key = Infinity;

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

    })
}
