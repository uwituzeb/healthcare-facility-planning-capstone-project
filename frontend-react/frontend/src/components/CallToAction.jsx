import React from "react";
import { Button } from "./buttons";
import { ArrowRight } from "lucide-react";

export const CallToAction = () => {
  return (
    <section className="py-20 px-4 bg-gradient-to-r from-[#004c99] to-[#686d72]">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
          Ready to Transform Healthcare Access?
        </h2>
        <p className="text-xl text-white/90 mb-10 leading-relaxed">
          Join healthcare providers and planners using AI-powered insights to
          make better infrastructure decisions and improve community health
          outcomes.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Button
            size="lg"
            className="bg-white text-[#004c99] hover:bg-gray-100 px-8 py-6 text-lg font-semibold h-auto"
          >
            Register Today
            <ArrowRight className="ml-2 w-5 h-5" />
          </Button>
        </div>
      </div>
    </section>
  );
};
