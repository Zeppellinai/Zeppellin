        

var words = ['Atsibodo tikrinti tamo pakeitimus?', 'Zeppellin tau gali padėti!', 'Zeppellin tai mokinio kurtas tvarkaraštis, kuris taupo duomenis bei laika!'],
part,
i = 0,
offset = 3,
len = words.length,
forwards = true,
skip_count = 0,
skip_delay = 60,
speed = 45;
var wordflick = function () {
setInterval(function () {
if (forwards) {
  if (offset >= words[i].length) {
    ++skip_count;
    if (skip_count == skip_delay) {
      forwards = false;
      skip_count = 0;
    }
  }
}
else {
  if (offset == 0) {
    forwards = true;
    i++;
    offset = 0;
    if (i >= len) {
      i = 0;
    }
  }
}
part = words[i].substr(0, offset);
if (skip_count == 0) {
  if (forwards) {
    offset++;
  }
  else {
    offset--;
  }
}
$('#text').text(part);
},speed);
};

$(document).ready(function () {
wordflick();
});

$(window).scroll(function() {
    if ($(this).scrollTop() > 200) { //use `this`, not `document`
        $('#scroll_down_indicator').css({
          'animation': 'none',
            'visibility': 'hidden',
            'opacity': '0',
            'transition': "visibility 0s 2s, opacity 2s linear"
        });
      // transition: ;
    //   $('#scroll_down_indicator').css({
    //     'animation': "none"
    // });
    //   for (let step = 100; step > 0; step = step - 1) {
    //     setTimeout(function() {
    //       console.log(step)
    //       $('#scroll_down_indicator').css({
    //         'opacity': step + "%"
    //     });
    //       //your code to be executed after 1 second
    //     }, 10);
    //     // Runs 5 times, with values of step 0 through 4.

    //   }
    
    }
});
