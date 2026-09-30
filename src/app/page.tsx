"use client"
import { House, SendHorizontal } from 'lucide-react'
import Image from 'next/image'
import React, { useState } from 'react'
import { Bricolage_Grotesque, JetBrains_Mono } from 'next/font/google'

const display = Bricolage_Grotesque({ subsets: ['latin'], weight: ['500', '700', '800'] })
const mono = JetBrains_Mono({ subsets: ['latin'], weight: ['400', '500'] })
const TICKS = 24

const page = () => {
  const [URL, setURL] = useState("")
  const [Data, setData] = useState(null)
  const [chances, setchances] = useState(0)

  const DetectPishing = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        url: URL
      })
    })

    const data = await res.json()
    console.log(data)
    setData(data)
    setchances(data.legitimate_probability)
  }

  const filled = Math.round((chances / 100) * TICKS)
  const color = chances >= 70 ? '#9bd77a' : chances >= 40 ? '#f3c26b' : '#ff5a4d'

  return (
    <div className={`${display.className} bg-[url(/mobilebg.jpg)] lg:bg-[url(/bg.png)] bg-cover bg-center bg-fixed bg-no-repeat bg-[#2b2016] min-h-dvh w-full text-[#fbe6b4]`}>
      <div className='mx-auto w-full max-w-6xl px-4 sm:px-10 pt-4'>
        <header className='w-full h-14 flex justify-between items-center rounded-xl bg-[#1c130d]/90 border border-[#c99a3b]/40 px-4'>
          <div className='flex items-center gap-3'>
            <Image
              src={"/logo.jpg"}
              width={36}
              height={36}
              className='rounded-full ring-2 ring-[#c99a3b]'
              alt='logo' />
            <span className='font-bold text-lg tracking-tight'>LinkCheck</span>
          </div>
          <div className='flex items-center gap-5 text-[#cdb38a]'>
            <House size={20} className='hover:text-[#fbe6b4] cursor-pointer' />
            <button className='hover:text-[#fbe6b4]'>About</button>
          </div>
        </header>
      </div>

      <main className='mx-auto w-full max-w-6xl px-4 sm:px-10 pt-14 sm:pt-24 pb-16'>
        <div className='max-w-xl flex flex-col gap-8'>
          <div className='flex flex-col gap-3'>
            <h1 className='text-5xl sm:text-7xl font-extrabold leading-[0.98] tracking-tight text-[#24150a]'>
              Check the link<br />before you click it.
            </h1>
            <p className='text-lg max-w-md text-[#4a2a10]'>
              Put your URL here and detect legitimate or not.
            </p>
          </div>

          <div className='flex flex-col rounded-xl bg-[#1c130d]/90 border border-[#c99a3b]/40 focus-within:border-[#c99a3b] transition-colors'>
            <div className='flex items-stretch'>
              <input
                onChange={(e) => { setURL(e.target.value) }}
                value={URL}
                type="text"
                spellCheck={false}
                className={`${mono.className} flex-1 min-w-0 bg-transparent px-4 py-4 text-sm sm:text-base outline-none placeholder:text-[#8a7050]`}
                placeholder='Put Url Here...' />
              <button
                onClick={DetectPishing}
                className='m-1.5 flex items-center gap-2 rounded-md bg-[#a3201e] border-b-4 border-[#c99a3b] px-4 font-bold text-[#fbe6b4] hover:bg-[#b82826] active:translate-y-0.5 active:border-b-2 transition-all'>
                Check <SendHorizontal size={18} />
              </button>
            </div>
            <p className='px-4 pb-3 text-sm text-[#ff9a8a]'>Note : Its Not 100% Correct Prediction</p>
          </div>

          <section
            className='flex flex-col gap-6 rounded-lg bg-[#1c130d]/90 p-5 border-l-4'
            style={{ borderLeftColor: color }}>
            <div className={`${mono.className} overflow-x-auto whitespace-nowrap rounded-md bg-black/30 px-4 py-3 text-sm sm:text-base text-[#cdb38a]`}>
              {URL || 'Your link will show here'}
            </div>

            <div>
              <div className='flex items-baseline gap-3 mb-3'>
                <span className='text-6xl font-extrabold leading-none' style={{ color }}>{chances}</span>
                <span className='text-[#cdb38a]'>
                  Legitimate Chances</span>
              </div>
              <div className='flex gap-1 h-10 items-end' role='img' aria-label={`Legitimate chances ${chances}`}>
                {Array.from({ length: TICKS }).map((_, i) => (
                  <div
                    key={i}
                    className='tick flex-1 rounded-xs origin-bottom'
                    style={{
                      height: `${40 + (i / TICKS) * 60}%`,
                      background: i < filled ? color : '#3a2c1f',
                      animation: `tick .25s ease-out ${i * 25}ms both`,
                    }}
                  />
                ))}
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  )
}

export default page