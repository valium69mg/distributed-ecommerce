
import InputForm from './InputForm'
import InputField from './InputField';
import { LiaEnvelopeSolid } from "react-icons/lia";
import { TbLockPassword } from "react-icons/tb";
import Button from './Button';
import { useState } from 'react';
import axios from 'axios';

const loginContainerStyle = {
    display: "flex",
    flexDirection: "column",
    width: "320px",
    height: "600px",
    border: "1px solid black",
    borderRadius: "6px",
    alignItems: "center"
}

export default function LoginForm() {

    const [loginData, setLoginData] = useState({
        email: "",
        password: "",
    });
    const [buttonActive, setButtonActive] = useState(true);

    function handleEmailChange(email) {
        setLoginData({
            ...loginData,
            email: email,
        })
    }

    function handlePasswordChange(password) {
        setLoginData({
            ...loginData,
            password: password,
        });
    }

    async function submit() {
        if (!buttonActive) return;
        setButtonActive(false);
        try {
            const response = await axios.post('http://ecommerce.local/auth/login', loginData);
            console.log(response.data);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setButtonActive(true);
            setLoginData({
            email: "",
            password: "",
            });
        }
    }


    return (
        <div style={loginContainerStyle}>
            <h1> LOGIN </h1>
            <InputForm inputField='Email'>
                <InputField placeHolder='Type your email' icon={<LiaEnvelopeSolid/>} value={loginData.email} onChange={handleEmailChange}/>
            </InputForm>
            <InputForm inputField='Password'>
                <InputField placeHolder='Type your password' icon={<TbLockPassword/>} value={loginData.password} onChange={handlePasswordChange}/>
            </InputForm>
            <Button buttonText='Login' onClick={submit}/>
        </div>
    )
}

