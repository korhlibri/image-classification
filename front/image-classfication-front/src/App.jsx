import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import HeaderTitle from './headerComponent'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <HeaderTitle/>
      
      <div>
        <form action="" method="post"></form>
        <button></button>
      </div>
    </>
  )
}

export default App
