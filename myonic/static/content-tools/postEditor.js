window.addEventListener('load', function() {
  function imageUploader(dialog) {
    var image, xhr, xhrComplete, xhrProgress;
    dialog.addEventListener('imageuploader.cancelupload', function() {
      // Cancel the current upload

      // Stop the upload
      if (xhr) {
        xhr.upload.removeEventListener('progress', xhrProgress);
        xhr.removeEventListener('readystatechange', xhrComplete);
        xhr.abort();
      }

      // Set the dialog to empty
      dialog.state('empty');
    });

    dialog.addEventListener('imageuploader.clear', function() {
      // Clear the current image
      dialog.clear();
      image = null;
    });

    dialog.addEventListener('imageuploader.fileready', function(ev) {

      // Upload a file to the server
      var formData;
      var file = ev.detail().file;

      // Define functions to handle upload progress and completion
      xhrProgress = function(ev) {
        // Set the progress for the upload
        dialog.progress((ev.loaded / ev.total) * 100);
      }

      xhrComplete = function(ev) {
        var response;

        // Check the request is complete
        if (ev.target.readyState != 4) {
          return;
        }

        // Clear the request
        xhr = null
        xhrProgress = null
        xhrComplete = null

        // Handle the result of the upload
        if (parseInt(ev.target.status) == 200) {
          // Unpack the response (from JSON)
          response = JSON.parse(ev.target.responseText);

          // Store the image details
          image = {
            size: response.size,
            url: response.url
          };

          // Populate the dialog
          dialog.populate(image.url, image.size);

        } else {
          // The request failed, notify the user
          new ContentTools.FlashUI('no');
        }
      }

      // Set the dialog state to uploading and reset the progress bar to 0
      dialog.state('uploading');
      dialog.progress(0);

      // Build the form data to post to the server
      formData = new FormData();
      formData.append('image', file);

      // Make the request
      xhr = new XMLHttpRequest();
      xhr.upload.addEventListener('progress', xhrProgress);
      xhr.addEventListener('readystatechange', xhrComplete);
      xhr.open('POST', '/admin/ajax/image/upload', true);
      xhr.send(formData);
    });

    function rotateImage(direction) {
      // Request a rotated version of the image from the server
      var formData;

      // Define a function to handle the request completion
      xhrComplete = function(ev) {
        var response;

        // Check the request is complete
        if (ev.target.readyState != 4) {
          return;
        }

        // Clear the request
        xhr = null
        xhrComplete = null

        // Free the dialog from its busy state
        dialog.busy(false);

        // Handle the result of the rotation
        if (parseInt(ev.target.status) == 200) {
          // Unpack the response (from JSON)
          response = JSON.parse(ev.target.responseText);

          // Store the image details (use fake param to force refresh)
          image = {
            size: response.size,
            url: response.url + '?_ignore=' + Date.now()
          };

          // Populate the dialog
          dialog.populate(image.url, image.size);

        } else {
          // The request failed, notify the user
          new ContentTools.FlashUI('no');
        }
      }

      // Set the dialog to busy while the rotate is performed
      dialog.busy(true);

      // Build the form data to post to the server
      formData = new FormData();
      formData.append('url', image.url);
      formData.append('direction', direction);

      // Make the request
      xhr = new XMLHttpRequest();
      xhr.addEventListener('readystatechange', xhrComplete);
      xhr.open('POST', '/admin/ajax/image/rotate', true);
      xhr.send(formData);
    }

    dialog.addEventListener('imageuploader.rotateccw', function() {
      rotateImage('CCW');
    });

    dialog.addEventListener('imageuploader.rotatecw', function() {
      rotateImage('CW');
    });

    dialog.addEventListener('imageuploader.save', function() {
      var crop, cropRegion, formData;

      // Define a function to handle the request completion
      xhrComplete = function(ev) {
        // Check the request is complete
        if (ev.target.readyState !== 4) {
          return;
        }

        // Clear the request
        xhr = null
        xhrComplete = null

        // Free the dialog from its busy state
        dialog.busy(false);

        // Handle the result of the rotation
        if (parseInt(ev.target.status) === 200) {
          // Unpack the response (from JSON)
          var response = JSON.parse(ev.target.responseText);

          // Trigger the save event against the dialog with details of the
          // image to be inserted.
          dialog.save(
            response.url,
            response.size, {
              // 'alt': response.alt,
              'data-ce-max-width': response.size[0]
            });

        } else {
          // The request failed, notify the user
          new ContentTools.FlashUI('no');
        }
      }

      // Set the dialog to busy while the rotate is performed
      dialog.busy(true);

      // Build the form data to post to the server
      formData = new FormData();
      formData.append('url', image.url);

      // Set the width of the image when it's inserted, this is a default
      // the user will be able to resize the image afterwards.
      formData.append('width', 600);

      // Check if a crop region has been defined by the user
      if (dialog.cropRegion()) {
        formData.append('crop', dialog.cropRegion());
      }

      // Make the request
      xhr = new XMLHttpRequest();
      xhr.addEventListener('readystatechange', xhrComplete);
      xhr.open('POST', '/admin/ajax/image/insert', true);
      xhr.send(formData);
    });
  }
  var editor;
  
  // =======================
  //        STYLES!
  // =======================
  ContentTools.StylePalette.add([
    // Image
    new ContentTools.Style('Big Brand Logo', 'big-brand-logo', ['img']),
    new ContentTools.Style('Responsive Image', 'img-responsive', ['img']),
    new ContentTools.Style('Circle Image (Requires perfectly square image)', 'img-circle', ['img']),
    new ContentTools.Style('Rounded Image', 'img-rounded', ['img']),
    // Animation
    new ContentTools.Style('Scroll Animation', 'animate'),
    new ContentTools.Style('Scroll Animation (sequence)', 'animate-seq'),
    // Modifiers
    new ContentTools.Style('Convert links to Buttons', 'btn', ['p']),
    // BS Table
    new ContentTools.Style('Bootstrap Table', 'table', ['table']),
    new ContentTools.Style('Bootstrap Striped Table', 'table-striped', ['table']),
    new ContentTools.Style('Bootstrap Hover Table', 'table-hover', ['table']),
    new ContentTools.Style('Bootstrap Table Green', 'success', ['tr', 'td']),
    new ContentTools.Style('Bootstrap Table Red', 'danger', ['tr', 'td']),
    new ContentTools.Style('Bootstrap Table Blue', 'info', ['tr', 'td']),
    new ContentTools.Style('Bootstrap Table Yellow', 'warning', ['tr', 'td']),
    new ContentTools.Style('Bootstrap Table Grey', 'active', ['tr', 'td']),
  ]);
  ContentTools.IMAGE_UPLOADER = imageUploader;
  editor = ContentTools.EditorApp.get();
  editor.init('*[data-editable], [data-fixture]', 'data-name');
  FIXTURE_TOOLS = [
    ['undo', 'redo', 'remove']
  ];
  ContentEdit.Root.get().bind('focus', function(element) {
    var tools;
    if (element.isFixed()) {
      tools = FIXTURE_TOOLS;
    } else {
      tools = ContentTools.DEFAULT_TOOLS;
    }
    if (editor.toolbox().tools() !== tools) {
      return editor.toolbox().tools(tools);
    }
  });

  editor.addEventListener('start', function(ev) {
    var _this = this;

    function autoSave() {
      _this.save(true);
    };
    this.autoSaveTimer = setInterval(autoSave, 30 * 1000);
  });

  editor.addEventListener('stop', function(ev) {
    clearInterval(this.autoSaveTimer);
  });

  function getImages() {
    // Return an object containing image URLs and widths for all regions
    var descendants, i, images;

    images = {};
    for (name in editor.regions()) {
      // Search each region for images
      descendants = editor.regions()[name].descendants();
      for (i = 0; i < descendants.length; i++) {
        // Filter out elements that are not images
        if (descendants[i].type() !== 'Image') {
          continue;
        }
        images[descendants[i].attr('src')] = descendants[i].size()[0];
      }
    }

    return images;
  }

  editor.addEventListener('saved', function(ev) {
    var name, onStateChange, passive, payload, regions, xhr;

    // Check if this was a passive save
    passive = ev.detail().passive;

    // Check to see if there are any changes to save
    regions = ev.detail().regions;
    console.log(ev.detail().regions);
    if (Object.keys(regions).length == 0) {
      return;
    }

    // Set the editors state to busy while we save our changes
    this.busy(true);

    // Collect the contents of each region into a FormData instance
    payload = new FormData();
    payload.append(
      'post_id',
      document.querySelector('meta[name="post_id"]')['content']
    );
    payload.append('images', JSON.stringify(getImages()));
    payload.append('regions', JSON.stringify(regions));

    // Send the update content to the server to be saved
    onStateChange = function(ev) {
      // Check if the request is finished
      if (ev.target.readyState == 4) {
        editor.busy(false);
        if (ev.target.status == '200') {
          // Save was successful, notify the user with a flash
          if (!passive) {
            new ContentTools.FlashUI('ok');
          }
        } else {
          // Save failed, notify the user with a flash
          new ContentTools.FlashUI('no');
        }
      }
    };

    xhr = new XMLHttpRequest();
    xhr.addEventListener('readystatechange', onStateChange);
    xhr.open('POST', '/admin/ajax/post/save');
    xhr.send(payload);
  });
});
