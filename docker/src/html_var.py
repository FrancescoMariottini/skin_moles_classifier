hello_html = '''<form action="login" method="POST">
                    hello world<br>
                    User Name : <input type="text" name="user"><br>                  
                    Password : <input type="text" name="pass"><br>                  
                    <input type="submit" value="Login"><br>
              </form>
              <script>/*complete this code to send dataa as JSON*/
              /*const data = new URLSearchParams();
                for (const pair of new FormData(formElement)) {
                    data.append(pair[0], pair[1]);}
                fetch(url, {method: 'post',
                            body: data,}).then(…);*/</script>'''
login_ok = '''<form action="predict" method="POST">
                    <br><br><br>
                    <div><div>
                            <div>Seller Avaible : </div>
                            <div><input type="text" name="seller_avaible"></div>
                        </div><br>
                        <div>
                            <div>Month : </div>
                            <div><input type="text" name="month"></div>
                        </div><br>
                        <div>
                            <div>Customer Visiting Website : </div>
                            <div><input type="text" name="customer_visiting_website"></div>
                        </div><br>
                  <input type="submit" value="Predict"><br>
                </form>
                <a href='image'> click here to go to image upload page</a>'''
image_upload = """
<!doctype html>
<title>Image Uploader</title>
<meta charset="utf-8" />
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.1/jquery-ui.min.js"></script>
<link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.1/themes/vader/jquery-ui.css" />
<h3>Image Uploader</h3>
<fieldset>
  <p id="status">Select an image</p>
  <div id="progressbar"></div>
  <input id="file" type="file" />
  <div id="drop">or drop image here</div>
</fieldset>
<fieldset>
  <p id="status">Click this button to see the result for the image below</p>  
  <button type="button" onclick="window.location.href='./predict';">Show me the Result!</button>  
</fieldset>
<div id="images">%s</div>
<script>
  function sse() {
      var source = new EventSource('/stream');
      source.onmessage = function(e) {
          if (e.data == '')
              return;
          var data = $.parseJSON(e.data);
          var upload_message = 'Image uploaded by ' + data['ip_addr'];
          var image = $('<img>', {alt: upload_message, src: data['src']});
          //call prediction by this photo
          //show predict result here
          var container = $('<div>').hide();
          container.append($('<div>', {text: upload_message}));
          container.append(image);
          $('#images').prepend(container);
          image.load(function(){
              container.show('blind', {}, 1000);
          });
      };
  }
  function file_select_handler(to_upload) {
      var progressbar = $('#progressbar');
      var status = $('#status');
      var xhr = new XMLHttpRequest();
      xhr.upload.addEventListener('loadstart', function(e1){
          status.text('uploading image');
          progressbar.progressbar({max: e1.total});
      });
      xhr.upload.addEventListener('progress', function(e1){
          if (progressbar.progressbar('option', 'max') == 0)
              progressbar.progressbar('option', 'max', e1.total);
          progressbar.progressbar('value', e1.loaded);
      });
      xhr.onreadystatechange = function(e1) {
          if (this.readyState == 4)  {
              if (this.status == 200)
                  var text = 'upload complete: ' + this.responseText;
              else
                  var text = 'upload failed: code ' + this.status;
              status.html(text + '<br/>Select an image');
              progressbar.progressbar('destroy');
          }
      };
      xhr.open('POST', '/post', true);
      xhr.send(to_upload);
  };
  function handle_hover(e) {
      e.originalEvent.stopPropagation();
      e.originalEvent.preventDefault();
      e.target.className = (e.type == 'dragleave' || e.type == 'drop') ? '' : 'hover';
  }
  $('#drop').bind('drop', function(e) {
      handle_hover(e);
      if (e.originalEvent.dataTransfer.files.length < 1) {
          return;
      }
      file_select_handler(e.originalEvent.dataTransfer.files[0]);
  }).bind('dragenter dragleave dragover', handle_hover);
  $('#file').change(function(e){
      file_select_handler(e.target.files[0]);
      e.target.value = '';
  });
  sse();
  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-510348-17']);
  _gaq.push(['_trackPageview']);
  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();
</script>
"""
