function DetectOut = Test_Detect(DetectIn)
    TrialData = DetectIn.("TrialData");
    TrainOut = DetectIn.("TrainOut");
    
    %plot(TrialData.("F3"))
    
    for j = 1:3
        x = rand(4*128, 14);
        y = fft(x);
    end
    
    x = round(rand(1)*1);

    if(x == 0)
        DetectOut = "RIGHT";
    else
        DetectOut = "LEFT";
    end
end
%{

function target = Test_Detect(DetectIn)
    %TrialData = DetectIn.("TrialData")
    %TrainOut = DetectIn.("TrainOut")
    
    %display(TrainOut)

    display("test")
    x = round(rand(1)*1)
    
    %y = [1 2 3]
    
    for x=1:100000
        y = rand(5)
        z = y / y
    end
    
    if(x == 0)
        target = "RIGHT"
    else
        target = "LEFT"
    end

    %target = TrainOut.W - TrainOut.Wo;
end
%}    
