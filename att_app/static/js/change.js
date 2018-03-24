var buttons = document.querySelectorAll('button');

[].forEach.call(buttons, function(btn) {
  btn.addEventListener('click', function() {
    var clickedButton = this;
    [].forEach.call(buttons, function(innerBtn) {
      if (innerBtn !== clickedButton) {
        innerBtn.classList.add('green');
      }
      else {
        innerBtn.classList.remove('green');
      }
    });
  });
});