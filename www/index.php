<!DOCTYPE html>
<html lang="ru">
 <head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>Joystick</title>
  <style type="text/css">
    html, body {
        height: 100%;
        margin: 0;
        padding: 0;
        overflow-x:hidden;
    }

    body{
        background-color: #2e2e2e;
    }

    .joyStick {
        margin: 500px auto;
        margin-bottom: 20px;
        width:200px; 
        height:200px; 
        background:#222121; 
        border:1px solid black;
        border-radius: 10px;
        border-width: 1px;
        position:relative;
    }

    .joyManipulator {
        width:40px;
        height:40px;
        position:absolute;
        border-radius:10px;
        background:rgb(206, 206, 206);
        cursor:pointer;
    }

    #panel {
        margin: 0 auto;
        width: 200px;
        background-color: #222121;
        border:1px solid black;
        border-radius: 10px;
        border-width: 1px;
    }

    #reset {
        padding: 10px;
        color: rgb(255, 255, 255);
        font-family: Arial;
        border:1px solid rgb(255, 255, 255);
        border-width: 1px;
        background-color: rgb(47, 47, 47);
        cursor: pointer;
    }

    #ox, #oy {
        margin: 0 auto;
        padding: 5px;
    }
 </style>
  <script src="joy.js"></script>
  <script src="jquery/jquery-1.9.1.js"></script>
  <script src="jquery/jquery-ui.js"></script>
  <link rel="stylesheet" href="style.css">
 </head>

 <body>

  <div id="joyStick" class="joyStick">
    <div class="joyManipulator"></div>
  </div>

  <div id = "panel">
    <center>
    <p>
    <input type="text" value="0" id="ox" /><br />
    <input type="text" value="0" id="oy" /><br /></p>
    <button id = "reset">reset</button><p>
    </center>
  </div>

 </body>
</html>