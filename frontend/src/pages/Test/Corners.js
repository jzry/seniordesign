import axios from "axios";
import { useEffect, useRef, useState } from "react";

function Corners() {
    // const [imageSrc, setImageSrc] = useState(null); // State to store the captured image
    // const [imageFile, setImageFile] = useState(null); // State to store the image file for API
    const canvasRef = useRef(null)
    const [image, setImage] = useState(null)


    const [corners, setCorners] = useState([
        { x: 50, y: 50 }, // Top-left
        { x: 400, y: 50 }, // Top-right
        { x: 400, y: 300 }, // Bottom-right
        { x: 50, y: 300 }, // Bottom-left
    ]);

    const [draggingCorner, setDraggingCorner] = useState(null);
    const [scale, setScale] = useState({ x: 1, y: 1 });

    function getMousePosition(e) {
        const { offsetX, offsetY } = e.nativeEvent;
        return {
            x: offsetX / scale.x,
            y: offsetY / scale.y
        };
    };

    function handleMouseUp() {
        setDraggingCorner(null);
    };

    function handleMouseMove(e) {
        if (draggingCorner !== null) {
            const { x, y } = getMousePosition(e);
            const newCorners = [...corners];
            newCorners[draggingCorner] = { x, y }
            setCorners(newCorners)
        }
    }

    function handleMouseDown(e) {
        const { x, y } = getMousePosition(e);
        console.log("Coordinates: [" + x + ", " + y + "]")
        const cornerIndex = corners.findIndex(
            (corner) => Math.hypot(corner.x - x, corner.y - y) < 25
        );
        console.log(cornerIndex)
        if (cornerIndex !== -1) {
            setDraggingCorner(cornerIndex);
        }
    }

    function drawQuad(context) {
        context.strokeStyle = "red";
        context.lineWidth = 10;
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
            context.arc(corner.x, corner.y, 24, 0, 2 * Math.PI)
            context.fill();
        });
    };

    function scaleCanvas(imgWidth, imgHeight) {
        const maxWidth = 800;
        const maxHeight = 600;
        let width = imgWidth;
        let height = imgHeight;

        if (width > maxWidth) {
            const scaleFactor = maxWidth / width;
            width = maxWidth;
            height = height * scaleFactor
        }

        if (height > maxHeight) {
            const scaleFactor = maxHeight / height;
            height = maxHeight;
            width = width * scaleFactor
        }

        return { width, height };
    }

    function drawToCanvas() {
        const canvas = canvasRef.current
        const context = canvas.getContext("2d")

        if (image) {
            const img = new Image();
            img.onload = () => {
                const {width, height} = scaleCanvas(img.naturalWidth, img.naturalHeight)
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;
                console.log(`Image dimensions: [${img.naturalWidth}, ${img.naturalHeight}]`)

                setScale({ x: width / img.naturalWidth, y: height / img.naturalHeight })

                canvas.style.width = `${width}px`
                canvas.style.height = `${height}px`

                context.drawImage(img, 0, 0);
                drawQuad(context)
            }
            img.src = image;
        } else {
            context.clearRect(0, 0, canvas.width, canvas.height);
        }
    }

    function handleFileChange(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                setImage(reader.result); // Set the image data URL
            };
            reader.readAsDataURL(file);
        }
    };

    useEffect(() => {
        drawToCanvas();
    }, [image, corners])



    return (
        <>
            <div className="container">
                <br /><br />

                <h4>
                    Upload the Business Card to Scan and Extract Entities
                </h4>

                <div className="row">
                    {/* <form> */}
                    <div className="input-group">
                        <input
                            type="file"
                            className="form-control"
                            name="image_name"
                            onChange={handleFileChange}
                            required />
                        {/* <input
                                type="submit"
                                value="Upload Image"
                                className="btn btn-primary"
                            // onClick={} 
                            /> */}
                    </div>
                    {/* </form> */}

                    <br />
                    {/* if fileupload */}
                    <div className="row">
                        <button className="btn btn-primary" id="sendData">Wrap Document and Extract Text</button>

                    </div>

                    {/* endif */}
                </div>

                {/* Creating Canvas */}
                {/* if fileupload */}

                <div className="row">
                    <div className="col">
                        <canvas
                            className="mt-5"
                            onMouseDown={handleMouseDown}
                            onMouseMove={handleMouseMove}
                            onMouseUp={handleMouseUp}
                            ref={canvasRef}
                            style={{cursor: "crosshair", maxWidth: "100%"}} />
                    </div>
                    {/* <div className="col" id="loader" align="center"> */}
                    {/* <img src={imageSrc} /> */}
                    {/* </div> */}
                </div>

                {/* {fileUpload && (
                    <>
                        <div className="row">
                            <div className="col">
                                <canvas id="canvas" style={{ "maxWidth": "100%" }} height="auto"></canvas>
                            </div>
                            <div className="col" id="loader" align="center">
                                <img src={imageSrc} />
                            </div>
                        </div>
                    </>
                )} */}

                {/* 
                    <script>
            loadPoints({{points | tojson}})
    */}

                {/* endif */}
            </div>
        </>
    )
}

export default Corners