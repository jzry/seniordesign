import axios from "axios";
import { useEffect, useRef, useState } from "react";

function Corners({ imageSrc, imageFile, onSubmitCorners }) {
    const canvasRef = useRef(null);
    const apiUrl = process.env.REACT_APP_API_URL;
    const [image, setImage] = useState(imageSrc);
    const [file, setFile] = useState(imageFile);
    const [hasCorners, setHasCorners] = useState(false);
    const [corners, setCorners] = useState(null);
    const [draggingCorner, setDraggingCorner] = useState(null);
    const [scale, setScale] = useState({ x: 1, y: 1 });

    function getMousePosition(e) {
        const { offsetX, offsetY } = e.nativeEvent;
        return {
            x: offsetX / scale.x,
            y: offsetY / scale.y
        };
    }

    function handleMouseDown(e) {
        const { x, y } = getMousePosition(e);
        if (!corners) return;
        const cornerIndex = corners.findIndex(
            (corner) => Math.hypot(corner.x - x, corner.y - y) < 20
        );
        if (cornerIndex !== -1) {
            setDraggingCorner(cornerIndex);
        }
    }

    function handleMouseMove(e) {
        if (draggingCorner !== null && corners) {
            const { x, y } = getMousePosition(e);
            const newCorners = [...corners];
            newCorners[draggingCorner] = { x, y };
            setCorners(newCorners);
        }
    }

    function handleMouseUp() {
        setDraggingCorner(null); // Allows dragging to continue after release
    }

    function drawQuad(context) {
        if (!corners) return;
        context.strokeStyle = "red";
        context.lineWidth = 4;
        context.beginPath();
        context.moveTo(corners[0].x, corners[0].y);
        for (let i = 1; i < corners.length; i++) {
            context.lineTo(corners[i].x, corners[i].y);
        }
        context.closePath();
        context.stroke();

        context.fillStyle = "blue";
        corners.forEach((corner) => {
            context.beginPath();
            context.arc(corner.x, corner.y, 10, 0, 2 * Math.PI);
            context.fill();
        });
    }

    function drawToCanvas() {
        const canvas = canvasRef.current;
        const context = canvas.getContext("2d");

        if (image) {
            const img = new Image();
            img.onload = () => {
                const { width, height } = scaleCanvas(img.naturalWidth, img.naturalHeight);
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;

                setScale({ x: width / img.naturalWidth, y: height / img.naturalHeight });

                canvas.style.width = `${width}px`;
                canvas.style.height = `${height}px`;

                context.drawImage(img, 0, 0);
                if (corners !== null) drawQuad(context);
            };
            img.src = image;
        } else {
            context.clearRect(0, 0, canvas.width, canvas.height);
        }
    }

    function scaleCanvas(imgWidth, imgHeight) {
        const maxWidth = 800;
        const maxHeight = 600;
        let width = imgWidth;
        let height = imgHeight;

        if (width > maxWidth) {
            const scaleFactor = maxWidth / width;
            width = maxWidth;
            height *= scaleFactor;
        }

        if (height > maxHeight) {
            const scaleFactor = maxHeight / height;
            height = maxHeight;
            width *= scaleFactor;
        }

        return { width, height };
    }

    async function submitImage(e) {
        e.preventDefault();
        if (file) {
            const formData = new FormData();
            formData.append("image", file);

            await axios
                .post(apiUrl.concat("/corners"), formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                })
                .then((response) => {
                    console.log("Extracted corners:", response.data.corner_points);
                    setCorners(response.data.corner_points);
                    setHasCorners(true);
                })
                .catch((error) => {
                    console.error("Could not extract corners!", error);
                    setCorners([
                        { x: 500, y: 500 },
                        { x: 1000, y: 500 },
                        { x: 1000, y: 1000 },
                        { x: 500, y: 1000 },
                    ]);
                    setHasCorners(true);
                });
        }
    }

    async function submitCorners(e, endpoint) {
        e.preventDefault();
        if (!corners || !file) return;
        
        const formData = new FormData();
        formData.append("image", file);
        formData.append("corners", JSON.stringify(corners));
    
        try {
            const response = await axios.post(apiUrl.concat(endpoint), formData, {
                headers: { "Content-Type": "multipart/form-data" }
            });
    
            console.log("Submitted corners response:", response.data);
    
            let processedData = response.data; // Extracting correct structure
    
            // Ensure correct extraction
            if (processedData && processedData.riderData) {
                onSubmitCorners(processedData);
            } else {
                console.error("Unexpected response format:", processedData);
            }
        } catch (error) {
            console.error("Error submitting corners:", error);
        }
    }
    
    

    useEffect(() => {
        drawToCanvas();
    }, [image, corners]);

    return (
        <>
            <link
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
                rel="stylesheet"
                integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
                crossOrigin="anonymous"
            />
            <div className="container">
                <br />
                <h4>Adjust Corners</h4>
                <div className="row">
                    <div className="col">
                        <canvas
                            className="mt-3"
                            onMouseDown={handleMouseDown}
                            onMouseMove={handleMouseMove}
                            onMouseUp={handleMouseUp}
                            ref={canvasRef}
                            style={{ cursor: "crosshair", maxWidth: "100%" }}
                        />
                    </div>
                </div>

                <br />

                {file && hasCorners && (
                    <div className="btn-group" role="group">
                        <button className="btn btn-primary" onClick={(e) => submitCorners(e, "/ctr")}>
                            Submit Corners CTR
                        </button>
                        <button className="btn btn-primary" onClick={(e) => submitCorners(e, "/bce")}>
                            Submit Corners BCE
                        </button>
                    </div>
                )}
                {!hasCorners && file && (
                    <button className="btn btn-primary" onClick={submitImage}>
                        Submit Image and Extract Corners
                    </button>
                )}
            </div>
            <script
                src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
                integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
                crossOrigin="anonymous"
            ></script>
        </>
    );
}

export default Corners;
