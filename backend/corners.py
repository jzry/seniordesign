def get_expected_corners(image_buffer):
    from preprocessing.scoresheet import Paper_Extraction

    # Perform paper extraction to get corners and warped image
    expected_corners = Paper_Extraction(image_buffer)

    if expected_corners == -1:
        return {"error": "Failed to process image"}

    # Extract corner points from the result
    corner_points = expected_corners.get("corner_points", [])
    corner_dict = {"corner_points": corner_points}  # Start with corner points in the output

    return corner_dict