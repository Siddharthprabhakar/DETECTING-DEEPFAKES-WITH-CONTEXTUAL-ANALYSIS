import { useEffect } from "react";
import AOS from "aos";
import "aos/dist/aos.css";

export default function Contact() {
  useEffect(() => {
    AOS.init({ duration: 1000 });
  }, []);
  
  return (
    <div className="py-24 sm:py-32" id="contact">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-xl leading-7">Who are we ?</h2>
          <p className="mt-2 text-4xl font-bold tracking-tight sm:text-6xl">
            About Us
          </p>
        </div>
        
        {/* Replace the form with your company information */}
        <div className="mt-16 max-w-xl mx-auto" data-aos="zoom-in">
          <p className="text-lg leading-7">
          We are Siddharth Prabhakar, Chahak Sengar, and Sumedh Dongre, final-year B.Tech students at Symbiosis Institute of Technology. This project marks a significant milestone in our academic journey as we strive to address complex challenges within our field.
          </p>
          <p className="mt-4 text-lg leading-7">
          In an age where deepfake technology poses ethical concerns, our mission is to safeguard authenticity in digital media. Our Deepfake Detection App is designed to empower users with the tools to identify and reduce the spread of misleading content. By leveraging advanced algorithms, we are committed to fostering a safer and more trustworthy online environment.
          </p>
        </div>
      </div>
    </div>
  );
}
