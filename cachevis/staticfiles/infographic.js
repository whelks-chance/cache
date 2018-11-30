// https://www.care.com/c/stories/6291/easy-homemade-cat-treats/

var sorted_data = [];
function record_line(line) {
    var thenumbers = line.match(/\d+/);
    if (thenumbers === null) {
        thenumbers = []
    }
    console.log(thenumbers + ' ' + thenumbers.length);
    sorted_data.push({
        'text': line,
        'numbers': thenumbers
    })
}

function do_infographics(sorted_data) {
    for (var i = 0, len = sorted_data.length; i < len; i++) {
        var payGraph = d3.select("#infographic_main").append("div")
            .attr("class", "infographic_single")
            .attr("id", i);

        var inner_text = payGraph.append("div")
            .attr("class", "infographic_text")
            .text(sorted_data[i].text)
    }
}

function getFile(file_url){

    $.ajax({
        url: file_url,
        success: function (data) {
            console.log(data.length);
            console.log(data);
            var lines = data.split("\n");
            for (var i = 0, len = lines.length; i < len; i++) {
                console.log(lines[i]);
                record_line(lines[i]);
            }
            // $('#raw_data').text(JSON.stringify(sorted_data));

            do_infographics(sorted_data);

        },
        type: 'text'
    });

}