
(function ($) {
  $.passGen = function (options) {
    options = $.extend({}, $.passGen.options, options);

    var charsets, charset = '', password = '', index;

    charsets = {
      'numeric'   : '0123456789',
      'lowercase' : 'abcdefghijklmnopqrstuvwxyz',
      'uppercase' : 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
      'special'   : '~!@#$%^&*()-+[]{}<>?'
    };

    $.each(charsets, function(key, value) {
      if (options[key]) {
        charset += value;
      }
    });

    for (var i=0; i< options.length; i++) {
      index = Math.floor(Math.random() * (charset.length));
      password += charset[index];
    }

    return password;
  };

  $.passGen.options = {
    'length' : 10,
    'numeric' : true,
    'lowercase' : true,
    'uppercase' : true,
    'special'   : false
  };
}(jQuery));
