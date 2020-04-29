#include "robotqt.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    RobotQt w;
    w.initialize();
    w.show();
    return a.exec();
}
