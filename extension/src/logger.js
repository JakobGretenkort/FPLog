function logAccess(object_name, property_name) {
  console.log(object_name, property_name);
}

function propertyLogger(object_name, property_name, value) {
  return () => {
    logAccess(object_name, property_name);
    return value;
  }
}

function functionLogger(object_name, function_name, replacement) {
  return (...args) => {
    logAccess(object_name, function_name);
    return replacement(...args);
  }
}

function registerPropertyLogger(object_name, property_name, object, value) {
  let logger = propertyLogger(object_name, property_name, value);
  Object.defineProperty(object, property_name, {
    get: logger
  });
}

function registerFunctionLogger(object_name, function_name, object, func) {
  let logger = functionLogger(object_name, function_name, func);
  Object.defineProperty(object, function_name, {
    value: (...args) => {return logger(...args)}
  });
}

function registerAllCanvas() {
  HTMLCanvasElement.prototype.toDataURL = function(...args) {
    logAccess("HTMLCanvasElement.prototype", "toDataURL");
    return this.toDataURLFPLog(...args);
  }

  HTMLCanvasElement.prototype.toBlob = function(...args) {
    logAccess("HTMLCanvasElement.prototype", "toDataURL");
    return this.toBlobFPLog(...args);
  }

  HTMLCanvasElement.prototype.getContext = function(contextType, ...args) {
    logAccess("HTMLCanvasElement.prototype", "getContext(" + contextType + ")");
    return this.getContextFPLog(contextType, ...args);
  }
}

function registerAllNavigator() {
  let appCodeName = navigator.appCodeName;
  registerPropertyLogger('navigator', 'appCodeName', navigator, appCodeName);

  let appName = navigator.appName;
  registerPropertyLogger('navigator', 'appName', navigator, appName);

  let appVersion = navigator.appVersion;
  registerPropertyLogger('navigator', 'appVersion', navigator, appVersion);

  let buildId = navigator.buildId;
  registerPropertyLogger('navigator', 'buildId', navigator, buildId);

  let cookieEnabled = navigator.cookieEnabled;
  registerPropertyLogger('navigator', 'cookieEnabled', navigator, cookieEnabled);

  let doNotTrack = navigator.doNotTrack;
  registerPropertyLogger('navigator', 'doNotTrack', navigator, doNotTrack);

  registerFunctionLogger('navigator', 'getGamepads', navigator, (...args) => {
    return navigator.getGamepadsFPLog(...args);
  });

  let hardwareConcurrency = navigator.hardwareConcurrency;
  registerPropertyLogger('navigator', 'hardwareConcurrency', navigator, hardwareConcurrency);

  let language = navigator.language;
  registerPropertyLogger('navigator', 'language', navigator, language);

  let languages = navigator.languages;
  registerPropertyLogger('navigator', 'languages', navigator, languages);

  let maxTouchPoints = navigator.maxTouchPoints;
  registerPropertyLogger('navigator', 'maxTouchPoints', navigator, maxTouchPoints);

  let mediaCapabilities = navigator.mediaCapabilities;
  registerPropertyLogger('navigator', 'mediaCapabilities', navigator, mediaCapabilities);

  let oscpu = navigator.oscpu;
  registerPropertyLogger('navigator', 'oscpu', navigator, oscpu);

  let platform = navigator.platform;
  registerPropertyLogger('navigator', 'platform', navigator, platform);

  let plugins = navigator.plugins;
  registerPropertyLogger('navigator', 'plugins', navigator, plugins);

  let productSub = navigator.productSub;
  registerPropertyLogger('navigator', 'productSub', navigator, productSub);

  let storage = navigator.storage;
  registerPropertyLogger('navigator', 'storage', navigator, storage);

  let userAgent = navigator.userAgent;
  registerPropertyLogger('navigator', 'userAgent', navigator, userAgent);

  let vendor = navigator.vendor;
  registerPropertyLogger('navigator', 'vendor', navigator, vendor);

  let vendorSub = navigator.vendorSub;
  registerPropertyLogger('navigator', 'vendorSub', navigator, vendorSub);

  let webdriver = navigator.webdriver;
  registerPropertyLogger('navigator', 'webdriver', navigator, webdriver);

  let cpuClass = navigator.cpuClass;
  registerPropertyLogger('navigator', 'cpuClass', navigator, cpuClass);
}

function registerAllScreen() {
  let availHeight = window.screen.availHeight;
  registerPropertyLogger('window.screen', 'availHeight', window.screen, availHeight);

  let availWidth = window.screen.availWidth;
  registerPropertyLogger('window.screen', 'availWidth', window.screen, availWidth);

  let width = window.screen.width;
  registerPropertyLogger('window.screen', 'width', window.screen, width);

  let height = window.screen.height;
  registerPropertyLogger('window.screen', 'height', window.screen, height);

  let colorDepth = window.screen.colorDepth;
  registerPropertyLogger('window.screen', 'colorDepth', window.screen, colorDepth);

  let pixelDepth = window.screen.pixelDepth;
  registerPropertyLogger('window.screen', 'pixelDepth', window.screen, pixelDepth);
}

function registerAllDocument() {
  registerFunctionLogger('document', 'createEvent', document, (type) => {
    if(type.trim().toLowerCase() == 'touchevent') {
      logAccess('document', 'createEvent("touchevent")');
    }
    return document.createEventFPLog(type);
  });

  document.addEventListener("DOMContentLoaded", function(event) {
    let body_clientWidth = document.body.clientWidth;
    registerPropertyLogger('document.body', 'clientWidth', document.body, body_clientWidth);
  });

  let documentElement_clientWidth = document.documentElement.clientWidth;
  registerPropertyLogger('document.documentElement', 'clientWidth',
    document.documentElement, documentElement_clientWidth);
}

function registerAllWindow() {
  registerFunctionLogger('window', 'matchMedia', window, (...args) => {
    return window.matchMediaFPLog(...args);
  });

  registerFunctionLogger('speechSynthesis', 'getVoices', speechSynthesis, (...args) => {
    return speechSynthesis.getVoicesFPLog(...args);
  });
}

function registerAll() {
  registerAllCanvas();
  registerAllNavigator();
  registerAllScreen();
  registerAllDocument();
  registerAllWindow();
}

registerAll();

