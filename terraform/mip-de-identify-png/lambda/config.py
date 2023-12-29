# AWS parameters
profile_name = ""
region_name = ""

# Data locations
png_bucket_name = ""
png_object_prefix = ""
png_object_name = ""
de_id_png_bucket_name = ""

# Pipeline parameters
dpi = 72
phi_detection_threshold = 0.00
redacted_box_color = 'red'

# Rekognition outputs
detected_texts_list = None
text_block = ""
total_length = 0
offset_array = [0,]
total_offsets = 1

# Comprehend Medical outputs
detected_phi_list = None
phi_scores_list = []
phi_texts_list = []
phi_types_list = []
phi_boxes_list = []
not_redacted = 0

