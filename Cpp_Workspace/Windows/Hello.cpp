#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;

int main()
{
    cout << "Hello World" << endl;
    cout << fixed; // �����ѧ������
    cout << setprecision(2); // ���þ���
    double number;
    number = 10.0/3*100000;
    /*
    * VS Code��Code Runner�������л������������
    * CMD���п�������ʾ
    */
    cout << "������λС����ֵΪ��" << number << endl; 
    return 0;
} 
