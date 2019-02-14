//$(document).ready(function () {
function getAngle(cx, cy, ex, ey, offset) {
  var dy = ey - cy;
  var dx = ex - cx;
  var theta = Math.atan2(dy, dx); // range (-PI, PI]
  theta *= 180 / Math.PI; // rads to degs, range (-180, 180]
  if (typeof offset != 'undefined')
		theta+=offset;
  if (theta < 0) theta = 360 + theta; // range [0, 360)
	
	return theta;
}
    //progressBarUpdate(90,100);
    progressBarUpdate(0,360);
    $('.pie').click(function(e){
//    function midiKnobUpdate(e){
//    function midiKnobUpdate(e){
       //progressBarUpdate(parseInt(Math.random()*100),100);
     var theThing = document.querySelector($(this).id);
     var container = document.querySelector('#contentContainer');
     var parentPosition = getPosition(e.currentTarget);
      
      
//     var xPosition = e.clientX - parentPosition.x - (theThing.clientWidth / 2);
//     var yPosition = e.clientY - parentPosition.y - (theThing.clientHeight / 2);

//     theThing.style.left = xPosition + "px";
//     theThing.style.top = yPosition + "px";
       var ex = e.clientX - parentPosition.x;
       var ey = e.clientY - parentPosition.y ;
      
//       var ex = e.clientX-$(this).offset().left;
//       var ey = e.clientY-$(this).offset().top;
       var ex2 = e.clientX;
       var ey2 = e.clientY;
       var cx = $(this).width()/2;
       var cy = $(this).height()/2;
       var angle = getAngle(cx, cy, ex, ey,90);
       $('.debug').text(ex + ' ' + ey + ' ' + cx  + ' ' + cy + ' DEG: ' + angle
        + $(this).offset().left + ' ' + $(this).offset().top + ' ' + ex2 + ' ' + ey2
//                        + xPosition + ' ' + yPosition
                       );
       progressBarUpdate(parseInt(angle),360);
    })
//    }
  
    function angle(cx, cy, ex, ey) {
      var dy = ey - cy;
      var dx = ex - cx;
      var theta = Math.atan2(dy, dx); // range (-PI, PI]
      theta *= 180 / Math.PI; // rads to degs, range (-180, 180]
      //if (theta < 0) theta = 360 + theta; // range [0, 360)
      return theta;
    }
   /* setInterval(function(){
      var val = parseInt($(".pie").attr('data-x'));
    	if (val < 100){
         val+=20;
      } else
				val = 0;
				progressBarUpdate(val,100);
    }, 600);
    */
//});

function rotate(element, degree) {
    element.css({
        '-webkit-transform': 'rotate(' + degree + 'deg)',
        '-moz-transform': 'rotate(' + degree + 'deg)',
        '-ms-transform': 'rotate(' + degree + 'deg)',
        '-o-transform': 'rotate(' + degree + 'deg)',
        'transform': 'rotate(' + degree + 'deg)',
        'zoom': 1
    });
}

function progressBarUpdate(x, outOf) {
    var firstHalfAngle = 180;
    var secondHalfAngle = 0;
    var oldAngle = parseInt($(".pie").attr('data-angle'));
    // caluclate the angle
    var drawAngle = x / outOf * 360;

    // calculate the angle to be displayed if each half
    if (drawAngle <= 180) {
        firstHalfAngle = drawAngle;
    } else {
        secondHalfAngle = drawAngle - 180;
    }
        
    if (drawAngle > 180 && oldAngle < 180){
       $(".slice1, .slice2").css({
      	'transition-duration':'0.15s',
        '-webkit-transition-duration':'0.15s'
      });
    	$(".slice1").css({
      	'transition-delay':'0s',
        '-webkit-transition-delay':'0s'
      });
      $(".slice2").css({
      	'transition-delay':'0.15s',
        '-webkit-transition-delay':'0.15s'
      });
    } else if (drawAngle < 180 && oldAngle > 180){
        $(".slice1, .slice2").css({
      	'transition-duration':'0.15s',
        '-webkit-transition-duration':'0.15s'
      });
    	$(".slice2").css({
      	'transition-delay':'0s',
        '-webkit-transition-delay':'0s'
      });
      $(".slice1").css({
      	'transition-delay':'0.15s',
        '-webkit-transition-delay':'0.15s'
      });
    } else {
      $(".slice1, .slice2").css({
      	'transition-delay':'0s',
        '-webkit-transition-delay':'0s',
        'transition-duration':'0.3s',
        '-webkit-transition-duration':'0.3s'
      });
    }
    
    $('.pie').attr('data-angle', drawAngle);
    $('.pie').attr('data-x', x);

    // set the transition
    rotate($(".slice1"), firstHalfAngle);
    rotate($(".slice2"), secondHalfAngle);

    // set the values on the text
    $(".status").html(x + " of " + outOf);
}


// Helper function to get an element's exact position
function getPosition(el) {
  var xPos = 0;
  var yPos = 0;

  while (el) {
    if (el.tagName == "BODY") {
      // deal with browser quirks with body/window/document and page scroll
      var xScroll = el.scrollLeft || document.documentElement.scrollLeft;
      var yScroll = el.scrollTop || document.documentElement.scrollTop;

      xPos += (el.offsetLeft - xScroll + el.clientLeft);
      yPos += (el.offsetTop - yScroll + el.clientTop);
    } else {
      // for all other non-BODY elements
      xPos += (el.offsetLeft - el.scrollLeft + el.clientLeft);
      yPos += (el.offsetTop - el.scrollTop + el.clientTop);
    }

    el = el.offsetParent;
  }
  return {
    x: xPos,
    y: yPos
  };
  
}