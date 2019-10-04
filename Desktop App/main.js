// Modules to control application life and create native browser window
const {app, BrowserWindow,session,globalShortcut} = require('electron')
const parseArgs = require('electron-args');



function addhttp(url) {
    if (!/^(?:f|ht)tps?\:\/\//.test(url)) {
        url = "http://" + url;
    }
    return url;
}



// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow

function createWindow () {
  // Create the browser window.
  mainWindow = new BrowserWindow({   

   
    fullscreen: false,
    kiosk: false,
    closable: true,
    alwaysOnTop: false,
    transparent: true,
    webPreferences: {
      devTools: true,     
    }

  })
  

  // and load the index.html of the app.
  if (cli.input[0] == undefined) {
  		mainWindow.loadFile('noarg.html')
  		setTimeout(()=>{
  			app.quit()
  		},5000)
  	}
    
  	else{
      url = addhttp(cli.input[0])
      
  		    mainWindow.loadFile('index.html')
          mainWindow.webContents.session.clearStorageData()
          setTimeout(()=>{ 	
          mainWindow.loadURL(url) 
          const cookie = { url: url, name: 'just_cause', value: 'tMgaCNOgpybhQL4jZOVoViuKRsRfUyVHN9JkmBU4h7Cf6tlT33zsdSb7MShmgini' }
          session.defaultSession.cookies.set(cookie)
          .then(() => {
            // success
          }, (error) => {
            console.error(error)
          }) 	
          },9000)
        

  	}
 

  

 


  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
  	mainWindow.onbeforeunload = (e) => {

  // Unlike usual browsers that a message box will be prompted to users, returning
  // a non-void value will silently cancel the close.
  // It is recommended to use the dialog API to let the user confirm closing the
  // application.
  e.returnValue = false // equivalent to `return false` but not recommended
}
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null
  })
}


// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.disableHardwareAcceleration(); 

const cli = parseArgs(`
    sample-viewer
 
    Usage
      $ sample-viewer [path]
 
    Options
      --help     show help
      --version  show version
      --auto     slide show [Default: false]
 
    Examples
      $ sample-viewer . --auto
      $ sample-viewer ~/Pictures/
`, {
    alias: {
        h: 'help'
    },
    default: {
        auto: false
    }
});
 

app.on('ready', function(){
	createWindow()

	globalShortcut.register('Alt+F4', function(){		
		console.log("SDfsdfsdfadsf")
	})
	globalShortcut.register('Alt+Tab', function(){		
		console.log("SDfsdfsdfadsf")
	})	
  globalShortcut.register('Super+d', function(){    
    console.log("SDfsdfsdfadsf")
  })  
	
	globalShortcut.register('CommandOrControl+Alt+q', function(){		
		app.quit();
	})
	
	globalShortcut.register('Alt+r', function(){		
		app.quit();
		app.relaunch();
	})

	


})
 app.on('browser-window-created',function(e,window) {
      window.setMenu(null);
  });

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') app.quit()
})

app.on('activate', function () {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) createWindow()
})


// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
