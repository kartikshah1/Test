_V_.Player.prototype.speed = 1.0;
_V_.ControlBar.prototype.options.components['speedButton'] = {};

_V_.Player.prototype.setSpeed = function(speed){
  this.tech.el.playbackRate = speed;
  this.speed = speed;
  this.triggerEvent ("speedchange");
};

_V_.speed2text = function (speed) {
  return Math.floor (speed) + '.' + Math.floor (speed * 10) % 10 + 'x';
}

_V_.SpeedMenuItem = _V_.MenuItem.extend({

  init: function(player, options){
    var speed = this.speed = options.speed;
    options.label = _V_.speed2text (speed);
    options.selected = (speed == 1.0);
    this._super(player, options);
    this.player.addEvent ("speedchange", _V_.proxy(this, this.update));
  },

  onClick: function(){
    this._super();
    this.player.setSpeed(this.speed);
  },

  update: function(){
    if (this.player.speed == this.speed) {
      this.selected(true);
    } else {
      this.selected(false);
    }
  }

});

_V_.RightMenu = _V_.Menu.extend({

  createElement: function(){
    return _V_.createElement("ul", {
      className: "vjs-menu vjs-menu-right"
    });
  }

});

_V_.SpeedButton = _V_.Button.extend({

  buttonText: "Speed",
  className: "vjs-speed-button",

  init: function(player, options){
    this._super(player, options);

    // Hide in Flash which does not support playbackRate.
    if (player.techName != 'html5') {
      this.el.style.display = 'none';
      return;
    }

    this.createMenu();

    this.text = _V_.createElement("span", { className: 'vjs-speed-text', innerHTML: '1.0x' });
    this.el.firstChild.appendChild(this.text);
    this.player.addEvent ("speedchange", _V_.proxy(this, this.update));
    // IE9 resets speed to 1.0x whenever playing; bugfix:
    this.player.addEvent ("play", _V_.proxy(this, function(){
      this.player.setSpeed(this.player.speed);
    }));
  },

  update: function(){
    this.text.innerHTML = _V_.speed2text (this.player.speed);
  },

  createMenu: function(){
    this.menu1 = new _V_.RightMenu(this.player);

    // Add a title list item to the top
    this.menu1.el.appendChild(_V_.createElement("li", {
      className: "vjs-menu-title",
      innerHTML: 'Speed'
    }));

    // Add menu items to the menu
    for (var i = 20; i > 5; i=i-2) {
      //if (i != 19 && i !== 17)
        this.menu1.addItem (new _V_.SpeedMenuItem (this.player, { speed: i / 10.0 }));
    }

    // Add list to element
    this.addComponent(this.menu1);
  },

  buildCSSClass: function(){
    return this.className + " vjs-menu-button " + this._super();
  },

  // Focus - Add keyboard functionality to element
  onFocus: function(){
    // Show the menu, and keep showing when the menu items are in focus
    this.menu1.lockShowing();
    // this.menu.el.style.display = "block";
  },
  // Can't turn off list display that we turned on with focus, because list would go away.
  onBlur: function(){},

  onClick: function(){
    // When you click the button it adds focus, which will show the menu indefinitely.
    // So we'll remove focus when the mouse leaves the button.
    // Focus is needed for tab navigation.
    this.one("mouseout", this.proxy(function(){
      this.menu1.unlockShowing();
      this.el.blur();
    }));
  }

});