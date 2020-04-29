#ifndef ROBOTQT_H
#define ROBOTQT_H

#include <QMainWindow>

namespace Ui {
class RobotQt;
}

class RobotQt : public QMainWindow
{
    Q_OBJECT

public:
    explicit RobotQt(QWidget *parent = 0);
    ~RobotQt();

    void initialize();
    void terminate();

private slots:
    void on_right_arm_slider_valueChanged(int value);

    void on_right_eye_slider_valueChanged(int value);

    void on_neck_LR_slider_valueChanged(int value);

    void on_left_eye_slider_valueChanged(int value);

    void on_left_arm_slider_valueChanged(int value);

    void on_neck_UD_slider_valueChanged(int value);

    void on_neck_slider_valueChanged(int value);

    void on_dance_button_clicked();

    void on_quit_button_clicked();

    void on_robot_address_returnPressed();

private:
    Ui::RobotQt *      ui;
    bool               connected_;
    QString            ip_;
    struct mosquitto * client_;

    void popup_message (const QString & msg, int r);
    void publish (const char * topic, float value);

};

#endif // ROBOTQT_H
