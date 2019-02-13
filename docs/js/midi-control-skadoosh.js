var knobHandler = function (knobID,containerID) {
  return function (event) {
    // event and extra_data will be available here
    
//    var theThing = document.querySelector(knobID);
//     var container = document.querySelector(containerID);
     var parentPosition = getPosition(event.currentTarget);
      
      
      //     var xPosition = event.clientX - parentPosition.x - (theThing.clientWidth / 2);
      //     var yPosition = event.clientY - parentPosition.y - (theThing.clientHeight / 2);

       var ex = event.clientX - parentPosition.x;
       var ey = event.clientY - parentPosition.y;

       var ex2 = event.clientX;
       var ey2 = event.clientY;
       var cx = $(this).width()/2;
       var cy = $(this).height()/2;
       var angle = getAngle(cx, cy, ex, ey,90);
       $('.debug').text(ex + ' ' + ey + ' ' + cx  + ' ' + cy + ' DEG: ' + angle
        + $(this).offset().left + ' ' + $(this).offset().top + ' ' + ex2 + ' ' + ey2
      //                        + xPosition + ' ' + yPosition
                       );
       progressBarUpdate(parseInt(angle),360,knobID);
  };
};

// Assign CallBacks - the arrows below point to numbers that change
//                          \/                                              \/       \/
document.getElementById('knob1').addEventListener("click", knobHandler('#knob1','#knob1_container'));
document.getElementById('knob2').addEventListener("click", knobHandler('#knob2','#knob2_container'));

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
    progressBarUpdate(0,360,0);

//    function midiKnobUpdate(event){
       //progressBarUpdate(parseInt(Math.random()*100),100);

  
function angle(cx, cy, ex, ey) {
  var dy = ey - cy;
  var dx = ex - cx;
  var theta = Math.atan2(dy, dx); // range (-PI, PI]
  theta *= 180 / Math.PI; // rads to degs, range (-180, 180]
  //if (theta < 0) theta = 360 + theta; // range [0, 360)
  return theta;
}
  

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

function progressBarUpdate(x, outOf,knobID) {
    var firstHalfAngle = 180;
    var secondHalfAngle = 0;
  if (knobID == 0) {
      var oldAngle = parseInt($(".pie").attr('data-angle')); 
    } else {
//      var theThing = document.querySelector(knobID);
      var oldAngle = parseInt($(document.querySelector(knobID)).attr('data-angle'));
    }
    
  
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
    
    if (knobID == 0) {
      $('.pie').attr('data-angle', drawAngle);
      $('.pie').attr('data-x', x);
    } else {
      $(document.querySelector(knobID)).attr('data-angle', drawAngle);
      $(document.querySelector(knobID)).attr('data-x', x);
//      var oldAngle = parseInt($(document.querySelector(knobID)).attr('data-angle'));
    }


    // set the transition
    if (knobID == 0) {
        rotate($(".slice1"), firstHalfAngle);
        rotate($(".slice2"), secondHalfAngle);
    } else {
      rotate($(document.querySelector(knobID+"_slice1")), firstHalfAngle);
      rotate($(document.querySelector(knobID+"_slice2")), secondHalfAngle);
//      $(document.querySelector(knobID+"_status")).html( 127*x/360 + " of " + 127*outOf/360);
    }


    // set the values on the text
    var midiRangeX = Math.floor(127*x/360 );
    var midiRangeOutOf = Math.floor(127*outOf/360);
    if (knobID == 0) {
        $(".status").html(midiRangeX + "/" + midiRangeOutOf);
    } else {

        $(document.querySelector((knobID+"_status"))).html(midiRangeX + "/" + midiRangeOutOf);
    }

    if (knobID != 0) {
        newMessage=getKnobValues();
        publishMIDIsettings(newMessage); // function defined in mqtt-skadoosh.js
    }
      

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

// Helper function that gets the values for all knob values
function getKnobValues() {
  var newMessage = "";
  newMessage += String(Math.floor(127* $(document.querySelector('#knob1')).attr('data-x') /360));
  newMessage +- ", ";
  newMessage += String(Math.floor(127* $(document.querySelector('#knob2')).attr('data-x') /360));
  return newMessage;
}

