function is_in(value, array){
    return array.indexOf(value) != -1;
}

//https://stackoverflow.com/a/19270021/2943238
function getRandom(arr, n) {
    var result = new Array(n),
        len = arr.length,
        taken = new Array(len);
    if (n > len)
        throw new RangeError("getRandom: more elements taken than available");
    while (n--) {
        var x = Math.floor(Math.random() * len);
        result[n] = arr[x in taken ? taken[x] : x];
        taken[x] = --len in taken ? taken[len] : len;
    }
    return result;
}


function build_radar(){

}

function radar_chart(url, div_id, ignore_list, data_title, legend_title){

    d3.csv(url).then(function(all_data) {

        // data = data.slice(0, 5);
        var data = getRandom(all_data, 5)
        console.log(data);

        var all_data_rearranged = [];
        var data_titles = [];

        for(var b in data) {

            var data_rearranged = [];
            var single_item = data[b];

            data_titles.push(single_item[data_title]);

            var keys_arr = Object.keys(single_item);
            console.log(keys_arr);

            for (var a in keys_arr) {
                var cleaned_value = clean_str2float_allow_nan(single_item[keys_arr[a]]);
                if (cleaned_value && !is_in(keys_arr[a], ignore_list)) {
                    data_rearranged.push({
                        'axis': keys_arr[a],
                        'value': cleaned_value
                    })
                }
            }

            all_data_rearranged.push(data_rearranged);
        }

        console.log(all_data_rearranged);

        /* Radar chart design created by Nadieh Bremer - VisualCinnamon.com */

        //////////////////////////////////////////////////////////////
        //////////////////////// Set-Up //////////////////////////////
        //////////////////////////////////////////////////////////////
        var margin = {top: 100, right: 100, bottom: 100, left: 100},
            width = Math.min(700, window.innerWidth - 10) - margin.left - margin.right,
            height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);

        console.log('got here pre radarChart 1')

        var color = d3.scaleOrdinal(d3.schemeCategory10)


        console.log('got here pre radarChart 2')

        var radarChartOptions = {
            w: width,
            h: height,
            margin: margin,
            maxValue: 0.5,
            levels: 5,
            roundStrokes: true,
            color: color,
            data_titles: data_titles,
            legend_title: legend_title
        };

        console.log('got here pre radarChart 3')

        RadarChart(div_id, all_data_rearranged, radarChartOptions);

    });

}