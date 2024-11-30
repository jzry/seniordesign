import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
    const navigate = useNavigate();

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [emailError, setEmailError] = useState('')
    const [passwordError, setPasswordError] = useState('')

    const handleGoBack = () => {
        navigate('/');
    }

    const onButtonClick = () => {
        console.log("Button has been clicked!")
    }

    return (
        <div>
            <div>
                <div>Login</div>
            </div>
            <br />
            <div>
                <input
                    value={email}
                    placeholder="Enter your email here"
                    onChange={(ev) => setEmail(ev.target.value)}
                />
                <label>{emailError}</label>
            </div>
            <br />
            <div>
                <input
                    value={password}
                    placeholder="Enter your password here"
                    onChange={(ev) => setPassword(ev.target.value)}
                />
                <label>{passwordError}</label>
            </div>
            <br />
            <div>
                <input type="button" onClick={onButtonClick} value={'Login'} />
            </div>
        </div>
    )
}

export default Login