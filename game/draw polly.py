import svgpathtools
import os

# Function to extract points from SVG path
def extract_points_from_svg(svg_file):
    # Load the SVG file and get the paths
    paths, attributes, svg_attributes = svgpathtools.svg2paths2(svg_file)
    
    # List to store coordinates
    polygon_points = []
    
    # Iterate through each path and extract points
    for path in paths:
        for segment in path:
            start = segment.start
            end = segment.end
            polygon_points.append((start.real, start.imag))  # start point (x, y)
            polygon_points.append((end.real, end.imag))      # end point (x, y)
    
    return polygon_points

# Path to the SVG file in the current directory
svg_file = os.path.join(os.getcwd(), 'Ear1.svg')  # Use current working directory to find the file

# Extract points from the SVG
polygon_points = extract_points_from_svg(svg_file)

# Print the extracted points for later use
print("Extracted Polygon Points:")
for point in polygon_points:
    print(point)

# Optionally, save the points to a file or process them further
