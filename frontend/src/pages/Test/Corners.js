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
        const isTouch = e.type.includes("touch");
        const clientX = isTouch ? e.touches[0].clientX : e.clientX;
        const clientY = isTouch ? e.touches[0].clientY : e.clientY;

        return {
            x: (clientX - left) / scale.x,
            y: (clientY - top) / scale.y
        };
    }

    function handlePointerDown(e) {
        e.preventDefault();
        if (!corners) return;
        const { x, y } = getMousePosition(e);

        const cornerIndex = corners.findIndex(
            (corner) => Math.abs(corner.x - x) < 40 && Math.abs(corner.y - y) < 40
        );

        if (cornerIndex !== -1) {
            setDraggingCorner(cornerIndex);
        }
    }

    function handlePointerMove(e) {
        e.preventDefault();
        if (draggingCorner === null || !corners) return;
        const { x, y } = getMousePosition(e);

        setCorners((prevCorners) => {
            if (!prevCorners) return prevCorners;
            const updatedCorners = [...prevCorners];
            updatedCorners[draggingCorner] = { x, y };
            return updatedCorners;
        });

        requestAnimationFrame(drawToCanvas);
    }

    function handlePointerUp(e) {
        e.preventDefault();
        setDraggingCorner(null);
    }

    function rotatePoint(point, width, height) {
        return {
            x: height - point.y, // Adjust X coordinate for 90-degree rotation
            y: point.x // Adjust Y coordinate
        };
    }

    function drawQuad(context, imgWidth, imgHeight) {
        if (!corners) return;

        // 🔥 Transform corner points for 90-degree rotation
        const rotatedCorners = corners.map((corner) =>
            rotatePoint(corner, imgWidth, imgHeight)
        );

        context.strokeStyle = "red";
        context.lineWidth = 4;
        context.beginPath();
        context.moveTo(rotatedCorners[0].x, rotatedCorners[0].y);
        for (let i = 1; i < rotatedCorners.length; i++) {
            context.lineTo(rotatedCorners[i].x, rotatedCorners[i].y);
        }
        context.closePath();
        context.stroke();

        context.fillStyle = "blue";
        rotatedCorners.forEach((corner) => {
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
                context.clearRect(0, 0, canvas.width, canvas.height);

                canvas.width = img.naturalHeight;
                canvas.height = img.naturalWidth;

                setScale({
                    x: img.naturalHeight / img.naturalWidth,
                    y: img.naturalWidth / img.naturalHeight
                });

                context.translate(canvas.width / 2, canvas.height / 2);
                context.rotate(90 * Math.PI / 180);
                context.drawImage(img, -img.naturalWidth / 2, -img.naturalHeight / 2);

                context.setTransform(1, 0, 0, 1, 0, 0);

                if (corners) {
                    drawQuad(context, img.naturalWidth, img.naturalHeight);
                }
            };
            img.src = image;
        } else {
            context.clearRect(0, 0, canvas.width, canvas.height);
        }
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
            submitImage();
        }
    }, [file]);

    useEffect(() => {
        requestAnimationFrame(drawToCanvas);
    }, [image, corners]);

    return (
        <>
            <link
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
                rel="stylesheet"
                integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXhW+ALEwIH"
                crossOrigin="anonymous"
            />
            <div className="container">
                <br />
                <h4>Adjust Corners</h4>
                <div className="row">
                    <div className="col">
                        <canvas
                            className="mt-3"
                            ref={canvasRef}
                            style={{ cursor: "crosshair", maxWidth: "100%" }}
                            onMouseDown={handlePointerDown}
                            onMouseMove={handlePointerMove}
                            onMouseUp={handlePointerUp}
                            onTouchStart={handlePointerDown}
                            onTouchMove={handlePointerMove}
                            onTouchEnd={handlePointerUp}
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
