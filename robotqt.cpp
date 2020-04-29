
#include <QDebug>
#include <mosquitto.h>
#include <QMessageBox>
#include <QHostAddress>

#include "iostream"
#include "robotqt.h"
#include "ui_robotqt.h"

RobotQt::RobotQt(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::RobotQt)
{
    ui->setupUi(this);

    connected_ = false;
    client_    = nullptr;
    mosquitto_lib_init ();
}

RobotQt::~RobotQt()
{
    mosquitto_lib_cleanup();
    delete ui;
}

void RobotQt::initialize()
{
    client_ = mosquitto_new ("WallE", true, (void *)this);
}
void RobotQt::terminate()
{
    if (connected_)
    {
        mosquitto_disconnect(client_);
        mosquitto_loop_stop(client_, true);
    }
    mosquitto_destroy (client_);
}
void RobotQt::on_right_arm_slider_valueChanged(int value)
{
    publish ("robot/body/right_arm/move", (float)value);
}

void RobotQt::on_right_eye_slider_valueChanged(int value)
{
    publish ("robot/head/right_eye/move", (float)value);
}

void RobotQt::on_neck_LR_slider_valueChanged(int value)
{
    publish ("robot/head/neck_LR/move", (float)value);
}

void RobotQt::on_left_eye_slider_valueChanged(int value)
{
    publish ("robot/head/left_eye/move", (float)value);
}

void RobotQt::on_left_arm_slider_valueChanged(int value)
{
    publish ("robot/body/left_arm/move", (float)value);
}

void RobotQt::on_neck_UD_slider_valueChanged(int value)
{
    publish ("robot/head/neck_UD/move", (float)value);
}

void RobotQt::on_neck_slider_valueChanged(int value)
{
    publish ("robot/body/neck/move", (float)value);
}

void RobotQt::on_dance_button_clicked()
{
    int r = mosquitto_publish(client_, nullptr, "robot/dance", 0, nullptr, 0, false);
    if (r != MOSQ_ERR_SUCCESS)
    {
        popup_message("unable to publish message to the robot at ip address \"" + ui->robot_address->text() + "\".", r);
    }
}

void RobotQt::on_quit_button_clicked()
{
    terminate();
    QApplication::quit();
}

void RobotQt::on_robot_address_returnPressed()
{
    int r;

    // get the new IP address.
    //
    QString ip = ui->robot_address->text();
    if (!ip.isEmpty())
    {
        // validate the IP address.
        //
        QHostAddress addr(ip);
        if (!addr.isNull())
        {
            // check if we are connected but connecting to a new host.
            //
            if (connected_ && (ip != ip_))
            {
                r = mosquitto_disconnect(client_);
                if (r == MOSQ_ERR_SUCCESS)
                {
                    // stop the MQTT loop.
                    //
                    mosquitto_loop_stop(client_, false);
                    connected_ = false;
                }
                else
                {
                    popup_message("unable to disconnect from robot at ip address \"" + ui->robot_address->text() + "\".", r);
                }
            }

            if (!connected_)
            {
                r = mosquitto_connect (client_, ip.toStdString().c_str(), 1883, 10);
                if (r == MOSQ_ERR_SUCCESS)
                {
                    // enable all buttons.
                    //
                    ui->left_arm_slider->setEnabled(true);
                    ui->left_eye_slider->setEnabled(true);
                    ui->neck_LR_slider->setEnabled(true);
                    ui->neck_UD_slider->setEnabled(true);
                    ui->neck_slider->setEnabled(true);
                    ui->right_arm_slider->setEnabled(true);
                    ui->right_eye_slider->setEnabled(true);
                    ui->dance_button->setEnabled(true);

                    // start the MQTT loop.
                    //
                    mosquitto_loop_start(client_);

                    // pop up a message.
                    //
                    popup_message("successfully connected to robot at ip address \"" + ui->robot_address->text() + "\".", r);

                    // store the IP address and mark as connected.
                    //
                    ip_ = ip;
                    connected_ = true;
                }
                else
                {
                    popup_message("unable to connect to robot at ip address \"" + ui->robot_address->text() + "\".", r);
                }
            }
        }
        else
        {
            popup_message("invalid ip address \"" + ui->robot_address->text() + "\".\n", -1);
        }
    }
}

void RobotQt::publish (const char * topic, float value)
{
    char payload[256];
    snprintf(payload, sizeof(payload), "%f", (float)value / 100.0);

    int r = mosquitto_publish(client_, nullptr, topic, strlen(payload), (const void *)payload, 0, false);
    if (r != MOSQ_ERR_SUCCESS)
    {
        popup_message("unable to publish message to the robot at ip address \"" + ui->robot_address->text() + "\".", r);
    }
}

void RobotQt::popup_message (const QString & msg, int r)
{
    QMessageBox msgBox(this);
    msgBox.setWindowTitle("WallE");
    if (r)
    {
        msgBox.setIcon(QMessageBox::Critical);
        if (r > 0)
        {
            msgBox.setText(msg + "\n" + mosquitto_strerror(r));
        }
        else
        {
            msgBox.setText(msg + "\n");
        }
    }
    else
    {
        msgBox.setText(msg + "\n");
    }
    msgBox.setStandardButtons(QMessageBox::Ok);
    msgBox.setDefaultButton(QMessageBox::Ok);
    msgBox.exec();
}



