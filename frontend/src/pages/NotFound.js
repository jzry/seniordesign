import { useNavigate } from 'react-router-dom'
import '../styles/NotFound.css'
import HorseImage from '../images/stop-horse.png'

// Component for the "404 Not Found" page
function NotFound()
{
    const navigate = useNavigate();
    
    const handleGoHome = () => {
        navigate('/')
    }
    
    return (
        <>
            <div className="not-found-container">
                <h>Whooaa, there!</h>
                <p>That page doesn't exist</p>
                <img src={HorseImage} alt="A horse standing next to a stop sign" />
                <button className="action-button" onClick={handleGoHome}>
                    Home
                </button>
            </div>
        </>
    )
}

export default NotFound
