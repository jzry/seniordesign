import axios from "axios";
import { useEffect, useRef, useState } from "react";

function Corners() {
    // const [imageSrc, setImageSrc] = useState(null); // State to store the captured image
    // const [imageFile, setImageFile] = useState(null); // State to store the image file for API
    const canvasRef = useRef(null)
    const [image, setImage] = useState(null)
    const apiUrl = process.env.REACT_APP_API_URL;
    const [imageFile, setImageFile] = useState(null); // State to store the image file for API
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
                const { width, height } = scaleCanvas(img.naturalWidth, img.naturalHeight)
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;
                console.log(`Image dimensions: [${img.naturalWidth}, ${img.naturalHeight}]`)

                setScale({ x: width / img.naturalWidth, y: height / img.naturalHeight })

                canvas.style.width = `${width}px`
                canvas.style.height = `${height}px`

                context.drawImage(img, 0, 0);
                if (corners !== null)
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
            setImageFile(file); // Store the image file for API submission
        }
    };

    async function submitImage(e) {


        e.preventDefault()
        if (imageFile) {
            const formData = new FormData();
            formData.append('image', imageFile);
            await axios.post(apiUrl.concat('/corners'), formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                }
            })
                .then((response) => {
                    console.log("Here are the new corners:")
                    setCorners(response.data.corner_points)
                    setHasCorners(true)
                })
                .catch((error) => {
                    console.error("Could no extract corners!")
                    console.error(error)
                    setCorners([
                        { x: 500, y: 500 },
                        { x: 1000, y: 500 },
                        { x: 1000, y: 1000 },
                        { x: 500, y: 1000 }
                    ])
                    setHasCorners(true)
                })
        }
    }

    async function submitCorners(e) {
        e.preventDefault()
        console.log("API URL:")
        console.log(apiUrl.concat('/corners'))
        console.log("Corners:")
        console.log({ 'corners': corners })
        // if (corners) {
            // await axios.post(apiUrl.concat('/corners'), { 'corners': corners })
                // .then((response) => {
                    // console.log(response.data.message)
                // })
                // .catch((error) => {
                    // console.error(error)
                // })
        // }
    }

    useEffect(() => {
        drawToCanvas();
    }, [image, corners])



    return (
        <>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous"></link>
            <div className="container">
                <br /><br />

                <h4>
                    Upload Image
                </h4>

                <div className="row">
                    {/* <form> */}
                    <div className="input-group">
                        <input
                            type="file"
                            className="form-control"
                            accept="image/*"
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
                        {(imageFile !== null && hasCorners) && <button className="btn btn-primary" id="sendData" onClick={submitCorners}>Submit Corners and Get Result</button>}
                        {(imageFile !== null && !hasCorners) && <button className="btn btn-primary" id="sendData" onClick={submitImage}>Submit Image and Extract Corners</button>}


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
                            style={{ cursor: "crosshair", maxWidth: "100%" }} />
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
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        </>
    )
}

export default Corners
