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
        const { left, top } = canvasRef.current.getBoundingClientRect();
        return {
            x: (e.clientX - left) / scale.x,
            y: (e.clientY - top) / scale.y
        };
    }

    function handleMouseDown(e) {
        if (!corners) return;
        const { x, y } = getMousePosition(e);

        // 🔥 Fix: Ensure right-side corners can also be detected
        const cornerIndex = corners.findIndex(
            (corner) => Math.abs(corner.x - x) < 30 && Math.abs(corner.y - y) < 30
        );

        if (cornerIndex !== -1) {
            setDraggingCorner(cornerIndex);
        }
    }

    function handleMouseMove(e) {
        if (draggingCorner === null || !corners) return;
        const { x, y } = getMousePosition(e);

        // Update only the dragged corner 🔥 Fix ensures all corners can move!
        setCorners((prevCorners) => {
            const updatedCorners = [...prevCorners];
            updatedCorners[draggingCorner] = { x, y };
            return updatedCorners;
        });

        drawToCanvas();
    }

    function handleMouseUp() {
        setDraggingCorner(null);
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
            context.arc(corner.x, corner.y, 20, 0, 2 * Math.PI);
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

    async function submitImage() {
        if (file) {
            const formData = new FormData();
            formData.append("image", file);

            try {
                const response = await axios.post(apiUrl.concat("/corners"), formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });

                console.log("Extracted corners:", response.data.corner_points);
                setCorners(response.data.corner_points);
                setHasCorners(true);
            } catch (error) {
                console.error("Could not extract corners!", error);
                setCorners([
                    { x: 500, y: 500 },
                    { x: 1000, y: 500 },
                    { x: 1000, y: 1000 },
                    { x: 500, y: 1000 },
                ]);
                setHasCorners(true);
            }
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

            if (response.data && response.data.riderData) {
                onSubmitCorners(response.data);
            } else {
                console.error("Unexpected response format:", response.data);
            }
        } catch (error) {
            console.error("Error submitting corners:", error);
        }
    }

    useEffect(() => {
        if (file) {
            submitImage(); // Auto-submit image when component receives it
        }
    }, [file]);

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
                        <button className="btn btn-primary" onClick={(e) => submitCorners(e, "/bce")}>
                            Submit Corners BCE
                        </button>
                    </div>
                )}
            </div>
        </>
    );
}

export default Corners;
