#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <strsafe.h>
#include <winuser.h>

#define to_clickx 142
#define to_clicky 337

#define print_coord(...) printf("%d,%d\n",__VA_ARGS__)

void normalize_coord(int *x,int *y){
    *x = *x * (65536 / GetSystemMetrics(SM_CXSCREEN));
    *y = *y * (65536 / GetSystemMetrics(SM_CYSCREEN));
}

typedef struct MOUSE_INPUT{
    INPUT i[3];
}MOUSE_INPUT;

/*
    _prep_click:-
        x:int      absolute pixel position<br>
        y:int      absolute pixel position<br>
        from:int[] array of mouseinput event each of right and left<br>
        len:int    length of from array<br>
*/
INPUT* _prep_click(int x,int y,int from[],int len){
    normalize_coord(&x,&y);
    INPUT *input = calloc(3,sizeof(INPUT));
    for(int i=0;i<len;i++){
        input[i].type = INPUT_MOUSE;
        input[i].mi.mouseData = 0;
        input[i].mi.dx = x;
        input[i].mi.dy = y;
        input[i].mi.dwFlags = MOUSEEVENTF_ABSOLUTE|from[i];
    }
    printf("[EVENT_TYPE](%x)\n",from[len-1]);
    return input;
}

INPUT *prep_click(DWORD ev ,int x,int y){
    int right[] = {MOUSEEVENTF_MOVE,MOUSEEVENTF_RIGHTDOWN,MOUSEEVENTF_RIGHTUP};
    switch(ev){
        case MOUSEEVENTF_LEFTDOWN|MOUSEEVENTF_LEFTUP:
            int left[] = {MOUSEEVENTF_MOVE,MOUSEEVENTF_LEFTDOWN,MOUSEEVENTF_LEFTUP};
            return _prep_click(x,y,left,3);
        case MOUSEEVENTF_LEFTDOWN:
            int left_down[] = {MOUSEEVENTF_MOVE,MOUSEEVENTF_LEFTDOWN};
            return _prep_click(x,y,left_down,2);
        case MOUSEEVENTF_LEFTUP:
            int left_up[] = {MOUSEEVENTF_MOVE,MOUSEEVENTF_LEFTUP};
            return _prep_click(x,y,left_up,2);
            
        case MOUSEEVENTF_RIGHTDOWN|MOUSEEVENTF_RIGHTUP:
            int right[] = {MOUSEEVENTF_MOVE,MOUSEEVENTF_RIGHTDOWN,MOUSEEVENTF_RIGHTUP};
            return _prep_click(x,y,right,3);
        case MOUSEEVENTF_RIGHTDOWN:
            int right_down[] = {MOUSEEVENTF_MOVE,MOUSEEVENTF_RIGHTDOWN};
            return _prep_click(x,y,right_down,2);
        case MOUSEEVENTF_RIGHTUP:
            int right_up[] = {MOUSEEVENTF_MOVE,MOUSEEVENTF_RIGHTUP};
            return _prep_click(x,y,right_up,2);
        case MOUSEEVENTF_MOVE:
            int move[] = {MOUSEEVENTF_MOVE};
            return _prep_click(x,y,move,1);
        default:
            _set_errno(1);
            return NULL;

    }

    

}

void printf_error(DWORD errn){
    LPSTR messageBuffer = NULL;
    size_t size = FormatMessageA(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
                                 NULL, errn, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), (LPSTR)&messageBuffer, 0, NULL);
    printf("%s\n",messageBuffer);

}

__declspec(dllexport) void moue_click(DWORD ev, int x, int y){
    INPUT *input = prep_click(ev,x,y);
    int c=SendInput(3, input, sizeof(INPUT));
    if(!c){
        DWORD error = GetLastError();
        printf_error(error);
    }
}

#ifndef NO_DEBUG

int main(int argc,char **argv) {
    // Find the window by its title (change "Window Title" to match the title of your target window)
    // HWND targetWindow = FindWindow(NULL, "a - Paint");
    HWND targetWindow = FindWindow(NULL, "Rush Royale");
    // Check if the window was found
    if (targetWindow == NULL) {
        printf("Window not found!\n");
        return 1;
    }
    if(argc<2){
        printf("Exiting..");
        return -1;
    }


    
    // Bring the window to the foreground
    SetForegroundWindow(targetWindow);
    int x=1,y=1;
    sscanf_s((++argv)[0],"%d",&x);
    sscanf_s((++argv)[0],"%d",&y);
    DWORD ev = MOUSEEVENTF_LEFTDOWN|MOUSEEVENTF_LEFTUP;
    moue_click(ev,x,y);        
    
}
#endif