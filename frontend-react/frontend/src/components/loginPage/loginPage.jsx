import React from "react";
import { SignupButton } from "../SignupButton";
import { Card, CardContent } from "../card";
import { Input } from "../input";

const LoginPage = () => {
  return (
    <div className="flex items-center justify-center min-h-screen w-full bg-[var(--signup-bg)]">
      <div className="flex gap-[5px]">
        <Card className="w-[417px] h-[525px] bg-[#ffffff2b] rounded-[30px_0px_0px_30px] border border-white backdrop-blur-[5px] backdrop-brightness-[100%] [-webkit-backdrop-filter:blur(5px)_brightness(100%)]">
          <CardContent className="flex items-center justify-center h-full p-0">
                      <div className="flex flex-col w-[339px] items-center gap-[42px]">
                        <div className="flex flex-col items-center w-full gap-2">
                          <h2 className="w-full [font-family:'Jost',Helvetica] font-semibold text-white text-xl text-center tracking-[0] leading-[normal]">
                  Welcome Back!
                </h2>
                <p className="w-full font-jost font-normal text-white text-sm text-center tracking-[0] leading-[normal]">
                  We're glad to see you again. Log in to access unparalleled
                  insights to revolutionize healthcare delivery.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="w-[417px] h-[525px] bg-[#ffffff2b] rounded-[0px_30px_30px_0px] border border-white backdrop-blur-[5px] backdrop-brightness-[100%] [-webkit-backdrop-filter:blur(5px)_brightness(100%)]">
          <CardContent className="flex items-center justify-center h-full p-0">
            <div className="flex flex-col w-[286px] items-center gap-[22px]">
              <div className="flex flex-col w-56 items-center">
                <h2 className="w-full font-jost font-semibold text-white text-xl text-center tracking-[0] leading-[normal]">
                  Sign in
                </h2>
              </div>

              <div className="flex flex-col items-center gap-[15px] w-full">
                <div className="flex flex-col items-center gap-7 w-full">
                  <div className="flex flex-col items-start gap-[31px] w-full">
                    <div className="flex flex-col items-start gap-2 w-full">
                      <Input
                        placeholder="Username"
                        className="w-full bg-[#ffffff4c] rounded-[5px] border border-white backdrop-blur-[2px] backdrop-brightness-[100%] [-webkit-backdrop-filter:blur(2px)_brightness(100%)] [font-family:'Jost',Helvetica] font-normal text-white text-sm tracking-[0] leading-[normal] placeholder:text-white h-auto px-[15px] py-2.5"
                      />
                      <Input
                        placeholder="Password"
                        type="password"
                        className="w-full bg-[#ffffff4c] rounded-[5px] border border-white backdrop-blur-[2px] backdrop-brightness-[100%] [-webkit-backdrop-filter:blur(2px)_brightness(100%)] [font-family:'Jost',Helvetica] font-normal text-white text-sm tracking-[0] leading-[normal] placeholder:text-white h-auto px-[15px] py-2.5"
                      />
                    </div>

                    <SignupButton className="w-full bg-[#00acff] rounded-[5px] backdrop-blur-[2px] backdrop-brightness-[100%] [-webkit-backdrop-filter:blur(2px)_brightness(100%)] [font-family:'Jost',Helvetica] font-medium text-white text-sm tracking-[0] leading-[normal] h-auto px-[15px] py-2.5 hover:bg-[#0099e6]">
                      Sign In
                    </SignupButton>
                  </div>
                </div>

                <p className="w-full font-jost font-normal text-white text-sm text-center tracking-[0] leading-[normal]">
                  Don't have an account?{" "}
                  <span className="font-bold cursor-pointer">Sign up</span>
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default LoginPage;
