import fs from 'fs';
import * as d3 from 'd3'; // Import D3 locally

// Function to generate the radial cluster SVG
async function generateRadialClusterSVG(cleanedData) {
    // Specify the chart’s dimensions
    const width = 500;
    const height = 500;
    const cx = width * 0.5; // Center x
    const cy = height * 0.54; // Center y
    const radius = Math.min(width, height) / 2 - 80;

    // Create a radial cluster layout
    const tree = d3.cluster()
        .size([2 * Math.PI, radius])
        .separation((a, b) => (a.parent === b.parent ? 1 : 2) / a.depth);

    // Sort the tree and apply the layout
    const root = tree(d3.hierarchy(cleanedData)
        .sort((a, b) => d3.ascending(a.data.name, b.data.name)));

    // Create the SVG elements manually
    let svgContent = `<svg width="${width}" height="${height}" viewBox="${-cx} ${-cy} ${width} ${height}" style="width: 100%; height: auto; font: 10px sans-serif;">`;

    // Append links
    svgContent += `<g fill="none" stroke="#555" stroke-opacity="0.5" stroke-width="0.5">`;
    root.links().forEach(link => {
        const d = d3.linkRadial()
            .angle(d => d.x)
            .radius(d => d.y)(link);
        svgContent += `<path d="${d}"/>`;
    });
    svgContent += `</g>`;

    // Append nodes
    svgContent += `<g>`;
    root.descendants().forEach(d => {
        svgContent += `<circle transform="rotate(${d.x * 180 / Math.PI - 90}) translate(${d.y},0)" fill="${d.children ? '#555' : '#999'}" r="0.5"/>`;
    });
    svgContent += `</g>`;

    // Append labels
    svgContent += `<g stroke-linejoin="round" stroke-width="3">`;
    root.descendants().forEach(d => {
        svgContent += `<text transform="rotate(${d.x * 180 / Math.PI - 90}) translate(${d.y - 1},0) rotate(${d.x >= Math.PI ? 180 : 0})" dy="0.31em" x="${d.x < Math.PI === !d.children ? 6 : -6}" text-anchor="${d.x < Math.PI === !d.children ? 'start' : 'end'}" paint-order="stroke" fill="white" font-size="5px">${d.data.name}</text>`;
    });
    svgContent += `</g>`;

    // Close the SVG tag
    svgContent += `</svg>`;

    // Return SVG as a string
    return svgContent;
}

function removeUrlNodes(data) {
    // Check if the data is an array
    if (Array.isArray(data)) {
        // Filter the array, recursively removing url nodes from children
        return data
            .map(removeUrlNodes) // Apply the function to each child
            .filter(node => !(node.type === "url")); // Remove nodes of type "url"
    } else if (typeof data === 'object' && data !== null) {
        // If it's an object, we need to process its children if they exist
        const { children, ...rest } = data; // Destructure to separate children
        const filteredChildren = children ? removeUrlNodes(children) : []; // Process children if they exist
        
        // Return the new object, excluding url nodes
        return { ...rest, children: filteredChildren };
    }
    // Return the data as is if it's neither an array nor an object
    return data;
}

// Save the SVG to a file
async function saveSVGToFile(filename) {
    const jsonData = fs.readFileSync('data.json', 'utf8');
    console.log(JSON.parse(jsonData));
    const cleanedData = removeUrlNodes(JSON.parse(jsonData)); // Parse JSON and access treatments
    const svgData = await generateRadialClusterSVG(cleanedData);
    fs.writeFileSync(filename, svgData, 'utf8');
    console.log(`SVG saved to ${filename}`);
}

// Call the save function
saveSVGToFile('radial-cluster.svg');
