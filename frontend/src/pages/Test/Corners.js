import axios from "axios";
import { useEffect, useRef, useState } from "react";

function Corners() {
    const canvasRef = useRef(null)
    const [image, setImage] = useState(null)
    const apiUrl = process.env.REACT_APP_API_URL;
    const [imageFile, setImageFile] = useState(null);
    const [hasCorners, setHasCorners] = useState(false);
    const [imageRes, setImageRes] = useState({ x: 0, y: 0 })
    const isRotated = useRef(false);
    const originalCorners = useRef(null)

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
        const cornerIndex = corners.findIndex(
            (corner) => Math.hypot(corner.x - x, corner.y - y) < 50
        );
        if (cornerIndex !== -1) {
            setDraggingCorner(cornerIndex);
        }
    }

    function drawQuad(context) {
        context.strokeStyle = "red";
        context.lineWidth = imageRes.x / 150;
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
            context.arc(corner.x, corner.y, imageRes.x / 50, 0, 2 * Math.PI)
            context.fill();
        });
    };

    function scaleCanvas(imgWidth, imgHeight) {
        const maxWidth = window.innerWidth * 0.7;
        const maxHeight = window.innerHeight * 0.7;
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
            img.src = image;
            img.onload = () => {
                setImageRes({ x: img.naturalWidth, y: img.naturalHeight })
                const { width, height } = scaleCanvas(img.naturalWidth, img.naturalHeight)

                if (width > height) {
                    isRotated.current = true;
                    setScale({ x: height / img.naturalHeight, y: width / img.naturalWidth })

                    canvas.width = img.naturalHeight;
                    canvas.height = img.naturalWidth;

                    canvas.style.width = `${height}px`
                    canvas.style.height = `${width}px`

                    context.clearRect(0, 0, canvas.width, canvas.height)
                    context.save();

                    context.translate(canvas.width, 0);
                    context.rotate(Math.PI / 2);


                    context.drawImage(img, 0, 0);

                    context.restore();

                    if (corners !== null)
                        drawQuad(context)
                }
                else {
                    setScale({ x: width / img.naturalWidth, y: height / img.naturalHeight })

                    canvas.width = img.naturalWidth;
                    canvas.height = img.naturalHeight;

                    canvas.style.width = `${width}px`
                    canvas.style.height = `${height}px`

                    context.clearRect(0, 0, canvas.width, canvas.height)
                    context.drawImage(img, 0, 0);
                    if (corners !== null)
                        drawQuad(context)
                }
            }
        } else {
            context.clearRect(0, 0, canvas.width, canvas.height);
        }
    }

    function handleFileChange(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                setImage(reader.result);
            };
            reader.readAsDataURL(file);
            setImageFile(file);
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
                    console.log("These are the corner values provided by preprocessing:")
                    console.log(response.data.corner_points)

                    if (isRotated.current) {
                        originalCorners.current = response.data.corner_points;
                        const corner = [
                            { x: imageRes.y - response.data.corner_points[0].y, y: response.data.corner_points[0].x },
                            { x: imageRes.y - response.data.corner_points[1].y, y: response.data.corner_points[1].x },
                            { x: imageRes.y - response.data.corner_points[2].y, y: response.data.corner_points[2].x },
                            { x: imageRes.y - response.data.corner_points[3].y, y: response.data.corner_points[3].x }
                        ]
                        setCorners(corner)
                        
                        console.log("These are the corner values AFTER the rotation has been applied:")
                        console.log(corner)
                    }
                    else
                        setCorners(response.data.corner_points);

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

    async function submitCornersCTR(e) {
        e.preventDefault()
        const formData = new FormData();
        formData.append('image', imageFile);

        if (corners) {
            if (isRotated.current) {
                console.log("These are the corner values BEFORE an inverse rotation is applied:")
                console.log(corners)

                formData.append("corners", JSON.stringify([
                    { x: corners[0].y, y: imageRes.y - corners[0].x },
                    { x: corners[1].y, y: imageRes.y - corners[1].x },
                    { x: corners[2].y, y: imageRes.y - corners[2].x },
                    { x: corners[3].y, y: imageRes.y - corners[3].x }
                ]));
            }
            else
                formData.append("corners", JSON.stringify(corners));

            console.log("These are the corner values that will be submitted to the backend:")
            console.log(JSON.parse(formData.get("corners")));

            await axios.post(apiUrl.concat('/ctr'), formData)
                .then((response) => {
                    console.log("Here is the rider data:")
                    console.log(response.data)
                })
                .catch((error) => {
                    console.error(error)
                })
        }
    }

    async function submitCornersBCE(e) {
        e.preventDefault()
        const formData = new FormData();
        formData.append('image', imageFile);

        if (corners) {
            if (isRotated.current) {
                console.log("These are the corner values BEFORE an inverse rotation is applied:")
                console.log(corners)

                formData.append("corners", JSON.stringify([
                    { x: corners[0].y, y: imageRes.y - corners[0].x },
                    { x: corners[1].y, y: imageRes.y - corners[1].x },
                    { x: corners[2].y, y: imageRes.y - corners[2].x },
                    { x: corners[3].y, y: imageRes.y - corners[3].x }
                ]));
            }
            else
                formData.append("corners", JSON.stringify(corners));

            console.log("These are the corner values that will be submitted to the backend:")
            console.log(JSON.parse(formData.get("corners")));

            await axios.post(apiUrl.concat('/bce'), formData)
                .then((response) => {
                    console.log("Here is the rider data:")
                    console.log(response.data)
                })
                .catch((error) => {
                    console.error(error)
                })
        }
    }

    useEffect(() => {
        drawToCanvas();
        window.addEventListener("resize", drawToCanvas);
        return () => window.removeEventListener("resize", drawToCanvas);
    }, [image, corners])



    return (
        <>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossOrigin="anonymous"></link>
            <div className="container">
                <br /><br />

                <h4>
                    Upload Image
                </h4>

                <div className="row">
                    <div className="input-group">
                        <input
                            type="file"
                            className="form-control"
                            accept="image/*"
                            name="image_name"
                            onChange={handleFileChange}
                            required />
                    </div>

                    <br />
                    <div className="row">
                        {(imageFile !== null && hasCorners) && (
                            <div className="btn-group" role="group" aria-label="Basic example">
                                <button className="btn btn-primary" id="sendData" onClick={submitCornersCTR}>Submit Corners CTR</button>
                                <button className="btn btn-primary" id="sendData" onClick={submitCornersBCE}>Submit Corners BCE</button>
                            </div>)}
                        {(imageFile !== null && !hasCorners) && <button className="btn btn-primary" id="sendData" onClick={submitImage}>Submit Image and Extract Corners</button>}


                    </div>

                </div>
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
                </div>

            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossOrigin="anonymous"></script>
        </>
    )
}

export default Corners
