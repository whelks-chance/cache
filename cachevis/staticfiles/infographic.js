// https://www.care.com/c/stories/6291/easy-homemade-cat-treats/

var sorted_data = [];
var font_names = [];

function record_line(line) {
    var thenumbers = [];

    // var regex = /[+-]?\d+(?:\.\d+)?/g;
    // var match;
    // while (match = regex.exec(line)) {
    //     thenumbers.push(match[0].replace(/[^\d.-]/g, ''));
    // }
    // .replace(",$", "").trim()

    // REGEX is hard - the below is a smashing together of the following plus trial and error
    // http://www.jquerybyexample.net/2012/02/extract-numbers-from-string-using.html
    // https://codereview.stackexchange.com/questions/115885/extract-numbers-from-a-string-javascript
    // https://stackoverflow.com/questions/5917082/regular-expression-to-match-numbers-with-or-without-commas-and-decimals-in-text

    var regex = /(:?^|\s)(?=.)((?:0|(?:[1-9](?:\d*|\d{0,2}(?:,\d{3})*)))?(?:\.\d*[1-9])?)(?!\S)/g;
    var match;
    while (match = regex.exec(line)) {
        thenumbers.push(match[0].trim());
    }

    if (thenumbers === null) {
        thenumbers = []
    }
    // console.log(thenumbers);

    thenumbers = Array.from(new Set(thenumbers))
    // console.log(thenumbers);
    sorted_data.push({
        'text': line,
        'numbers': thenumbers
    })
}

function get_icon_class(text) {
    var randomNumber = Math.floor(
        Math.random() * font_names.length
    );
    return "infographic_icon fa fa-4x fa-" + font_names[randomNumber];
}

function get_random_color(){
    return "hsl(" + Math.random() * 360 + ",100%,50%)";
}

var randomColor = function(){
    // http://bl.ocks.org/jdarling/06019d16cb5fd6795edf
    var golden_ratio_conjugate = 0.618033988749895;
    var h = Math.random();

    var hslToRgb = function (h, s, l){
        var r, g, b;

        if(s == 0){
            r = g = b = l; // achromatic
        }else{
            function hue2rgb(p, q, t){
                if(t < 0) t += 1;
                if(t > 1) t -= 1;
                if(t < 1/6) return p + (q - p) * 6 * t;
                if(t < 1/2) return q;
                if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
                return p;
            }

            var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
            var p = 2 * l - q;
            r = hue2rgb(p, q, h + 1/3);
            g = hue2rgb(p, q, h);
            b = hue2rgb(p, q, h - 1/3);
        }

        return '#'+Math.round(r * 255).toString(16)+Math.round(g * 255).toString(16)+Math.round(b * 255).toString(16);
    };

    h += golden_ratio_conjugate;
    h %= 1;
    return hslToRgb(h, 0.5, 0.60);
};

var layout_classes = [
    ["default", "infographic_single_default_inner"],
    ["infographic_single_backwards", "infographic_single_backwards_inner"],
    ["infographic_single_right", "infographic_single_right_inner"]
];

function get_infographic_single_classes(text) {
    var randomNumber = Math.floor(Math.random() * layout_classes.length);
    var class_group = layout_classes[randomNumber];
    return [
        "infographic_single " + class_group[0],
        "infographic_single_inner_group " + class_group[1]
    ];
}

function do_infographics(sorted_data) {
    for (var i = 0, len = sorted_data.length; i < len; i++) {
        if (sorted_data[i].numbers.length) {

            var color = randomColor();

            var infographic_single_classes = get_infographic_single_classes(sorted_data[i].text);

            var infographic_single = d3.select("#infographic_main").append("div")
                .attr("class", infographic_single_classes[0])
                .attr("id", i).attr("data-len", sorted_data[i].text.length);

            if (sorted_data[i].text.length > 100) {
                infographic_single.style("flex-grow", 3)
            } else {
                infographic_single.style("flex", 1)
            }
            // infographic_single.style("flex-grow", Math.pow(sorted_data[i].text.length / 100, 10));

            var inner_text = infographic_single.append("div")
                .attr("class", "infographic_text")
                .text(sorted_data[i].text)
                .style("color", color)

            var inner_group = infographic_single.append("div")
                .attr("class", infographic_single_classes[1]);

            for (var j = 0, jlen = sorted_data[i].numbers.length; j < jlen; j++) {

                var inner_number = inner_group.append("div")
                    .attr("class", "infographic_number")
                    .text(sorted_data[i].numbers[j])
                    .style("color", color)
            }

            var icon_class = get_icon_class(sorted_data[i].text);
            var inner_icon = inner_group.append("i")
                .attr("class", icon_class)
                .style("color", color)
        }
    }
}

function get_font_file(font_name_url, data_url, get_data_file_and_build){
    $.ajax({
        url: font_name_url,
        success: function (data) {
            console.log(data.length);
            var lines = data.split("\n");
            for (var i = 0, len = lines.length; i < len; i++) {
                font_names.push(lines[i]);
            }
            // console.log(font_names);
            get_data_file_and_build(data_url);
        },
        type: 'text'
    });

}

function get_data_file_and_build(data_url) {
    $.ajax({
        url: data_url,
        success: function (data) {
            // console.log(data.length);
            // console.log(data);
            var lines = data.split("\n");
            for (var i = 0, len = lines.length; i < len; i++) {
                // console.log(lines[i]);
                record_line(lines[i]);
            }
            // $('#raw_data').text(JSON.stringify(sorted_data));

            do_infographics(sorted_data);

        },
        type: 'text'
    });
}

function build_infographic(data_url, font_name_url){

    get_font_file(font_name_url, data_url, get_data_file_and_build);

}