//Define editor option and styling
const TINYMCE_OPTIONS = {
    selector: 'textarea',
    'menubar': '',
    'plugins': 'link image code fullscreen template visualblocks fullpage paste hr preview',
    'toolbar': 'bold italic paste styleselect | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image hr | code view preview | visualblocks | template ',
    'automatic_uploads': true,
    'image_title': true,
    'images_upload_url': '/api/v1/file-uploads/',
    'file_picker_types': 'image',
    'file_picker_callback': function(cb, value, meta){
        console.log([cb, value, meta]);
        var input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');

        // Note: In modern browsers input[type="file"] is functional without
        // even adding it to the DOM, but that might not be the case in some older
        // or quirky browsers like IE, so you might want to add it to the DOM
        // just in case, and visually hide it. And do not forget do remove it
        // once you do not need it anymore.

        input.onchange = function() {
          var file = this.files[0];

          // Note: Now we need to register the blob in TinyMCEs image blob
          // registry. In the next release this part hopefully won't be
          // necessary, as we are looking to handle it internally.
          var id = 'blobid' + (new Date()).getTime();
          var blobCache = tinymce.activeEditor.editorUpload.blobCache;
          var blobInfo = blobCache.create(id, file);
          blobCache.add(blobInfo);

          // call the callback and populate the Title field with the file name
          cb(blobInfo.blobUri(), { title: file.name });
        };

        input.click();
    },
    'height': 500,
    'templates': [
        {
            'title': 'Submission number',
            'description': 'Display submission number',
            'content': '{{SUBMISSION_NUMBER}}'
        }
    ]
};