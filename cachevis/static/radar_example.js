function is_in(value, array){
    return array.indexOf(value) != -1;
}

var ignore_list = [
    "OS Grid Easting",
    "OS Grid Northing",
    "NLC",
    "Large station change flag"
];

function radar_chart(url, div_id){

    d3.csv(url).then(function(data) {

        data = data.slice(0, 5);
        console.log(data);

        var all_data_rearranged = [];
        var data_titles = [];

        for(var b in data) {

            var data_rearranged = [];
            var single_item = data[b];

            data_titles.push(single_item['Station Name']);

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
            data_titles: data_titles
        };

        console.log('got here pre radarChart 3')

        RadarChart(div_id, all_data_rearranged, radarChartOptions);

    });

}