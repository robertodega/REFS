<?php
header('Content-type: image/jpeg');
header('Content-Disposition: attachment; filename="downloaded_image.jpg"');
readfile('./sample_image.jpg');
?>