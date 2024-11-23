import { faArrowPointer } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import React, { useState, useEffect, useRef } from 'react';

export const ReplayFeed = () => {
    const [mouseData, setMouseData] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const squareRef = useRef(null);
    const wrapperRef = useRef(null);
    const iframeRef = useRef(null);

    useEffect(() => {
        fetch('/logs.json')
            .then((response) => response.json())
            .then((data) => {
                setMouseData(data);
            });
    }, []);

    // Works
    useEffect(() => {
        if (mouseData.length === 0) return;

        const startTime = new Date(mouseData[0].timestamp).getTime();
        const endTime = new Date(mouseData[mouseData.length - 1].timestamp).getTime();
        const totalDuration = endTime - startTime;
        let currentTime = startTime;

        const interval = setInterval(() => {
            if (currentIndex < mouseData.length - 1) {
                const nextTime = new Date(mouseData[currentIndex + 1].timestamp).getTime();
                const timeDifference = nextTime - currentTime;
                currentTime = nextTime;
                setCurrentIndex(currentIndex + 1);

                const currentMouseData = mouseData[currentIndex];
                const nextMouseData = mouseData[currentIndex + 1];

                const square = squareRef.current;
                const wrapper = wrapperRef.current;

                if (wrapper) {
                    if (nextMouseData.scrollX == undefined || nextMouseData.scrollY == undefined) {
                        wrapper.style.width = `${nextMouseData.width}px`;
                        wrapper.style.height = `${nextMouseData.height}px`;
                    }

                }

                if (square) {
                    square.style.left = `${nextMouseData.x}px`;
                    square.style.top = `${nextMouseData.y}px`;
                }
            } else {
                clearInterval(interval);
            }
        }, 100);

        return () => clearInterval(interval);
    }, [mouseData, currentIndex]);


    // Comment out this useEffect for the scroll to stop applying. Currently Broken
    useEffect(() => {
        if (mouseData.length === 0) return;

        const nextMouseData = mouseData[currentIndex];

        const wrapper = wrapperRef.current;
        const iframe = iframeRef.current;

        if (wrapper && nextMouseData) {
            console.log('here')
            wrapper.style.width = `${nextMouseData.width}px`;
            wrapper.style.height = `${nextMouseData.height + (nextMouseData.scrollY || 0)}px`;

            if (nextMouseData.scrollX !== undefined || nextMouseData.scrollY !== undefined) {

                if (nextMouseData.scrollY !== undefined) {
                    iframe.style.marginTop = `-${nextMouseData.scrollY}px`;
                    const newHeight = parseInt(wrapper.style.height) + nextMouseData.scrollY;
                    wrapper.style.height = `${newHeight}px`;
                }
            }
        }
    }, [mouseData, currentIndex]);

    return (
        <div className='h-screen w-screen relative'>
            <div
                ref={wrapperRef}
                className='absolute border bg-white'
                style={{
                    left: '0px',
                    top: '0px',
                    transition: 'width 0.1s, height 0.1s',
                    overflow: 'hidden',
                }}
            >
                <iframe
                    ref={iframeRef}
                    title="Embedded Site"
                    src="https://www.riamoneytransfer.com/en-us/"
                    width="100%"
                    height="100%"
                    style={{ border: 'none', top: 0, left: 0 }}
                />
                <FontAwesomeIcon
                    ref={squareRef}
                    icon={faArrowPointer}
                    className='absolute h-4 w-4 z-20 text-black'
                    style={{
                        left: `${mouseData[currentIndex]?.x}px`,
                        top: `${mouseData[currentIndex]?.y}px`,
                        transition: 'left 0.1s, top 0.1s'
                    }}
                />
            </div>
        </div>
    );
};
