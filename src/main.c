#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <strsafe.h>



void moue_click(int x, int y){
    INPUT input;
    input.type = INPUT_MOUSE;
    input.mi.mouseData = 0;
    input.mi.dx = x * (65536 / GetSystemMetrics(SM_CXSCREEN)); //x being coord in pixels
    input.mi.dy =  y * (65536 / GetSystemMetrics(SM_CYSCREEN)); //y being coord in pixels
    input.mi.dwFlags = MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE;
    int c = SendInput(1, &input, sizeof(input));
    if(!c)
        printf("Some Error Occured");
    input.mi.dwFlags = MOUSEEVENTF_ABSOLUTE |MOUSEEVENTF_LEFTDOWN;
    c=SendInput(1, &input, sizeof(input));;
     if(!c)
        printf("Some Error Occured");
    printf("Send INput was {%d}",c);
    Sleep(0.1);
    input.mi.dwFlags = MOUSEEVENTF_ABSOLUTE |MOUSEEVENTF_LEFTUP;
    c=SendInput(1, &input, sizeof(input));
    printf("Send INput was {%d}",c);
     if(!c)
        printf("Some Error Occured");
    printf("Send INput was {%d}",c);
}

int main() {
    // Find the window by its title (change "Window Title" to match the title of your target window)
    HWND targetWindow = FindWindow(NULL, "a - Paint");
    
    // Check if the window was found
    if (targetWindow == NULL) {
        printf("Window not found!\n");
        return 1;
    }

    
    // Bring the window to the foreground
    SetForegroundWindow(targetWindow);
    int x=1,y=1;
    for(int i=0;i<10;i++){
        x =  (100+i);
        y =  (100+i);
        moue_click(x,y);
        
        printf("%d|%d\n",x,y);
        Sleep(0.1);
    }
    
    // Send the input
    
    return 0;
}
